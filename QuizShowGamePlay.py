#!/usr/bin/env python2.7

import sys, os, signal
import datetime
from sqlalchemy import create_engine
import time
from threading import Thread, Event, Lock, Timer
from display import Display
from gpio32.lib import Manager
from flask import Flask, request
import configparser
import json
import inspect

# Event object used to send signals from one thread to another
stopGameEvent = Event()
Boards = Manager()
api = Flask(__name__)

class Config(object):

    def __init__(self):
        self._config = configparser.ConfigParser()
        self._config.read('config.cfg')

        sec = self._config['DEFAULT']
        self.RoundTime = int(sec['ROUND_TIME'])
        self.GameTime = int(sec['GAME_TIME'])
        self.BoardStack = sec['BOARD_STACK'].split(',')
        self.IncScore = int(sec['INC_SCORE'])
        self.DecScore = int(sec['DEC_SCORE'])
        self.InitScore = int(sec['INIT_SCORE'])
        self.DB_URL = sec['DB_URL']
        self.InviteSleep = int(sec['INVITE_SLEEP'])
        self.BoardPlayerLimit = int(sec['BOARD_PLAYER_LIMIT'])
        self.Display_Host = sec['DISP_HOST']
        self.Me_Host = sec['ME_HOST']


C = Config()

D = Display(C.Display_Host)
D.setGameTimer(C.GameTime)

class Button():

    def __init__(self, board, pin_in, pin_out):
        self._board = board
        self._in = pin_in
        self._out = pin_out

    def light(self, on=True):
        if on:
            self._board.turnOn(self._out)
        else:
            self._board.turnOff(self._out)

    def hook(self, h):
        self._board.onChange(h, self._in)

    def read(self):
        return self._board.readPin(self._in)

    def clearHooks(self):
        self._board.clearHooks()

global _choices
_choices = ['red', 'green', 'yellow', 'blue']
class Player():
    
    def __init__(self, board, bot):
        global _choices
        self.buttons = { l: Button(board, i, i + 1) for l, i in zip( _choices, range(bot, bot + 8, 2) ) }
        self._board = board

    def lightAll(self, on=True):
        for b in self.buttons:
            self.buttons[b].light(on)

    def __getitem__(self, x):
        return self.buttons[x]

    def catchAnswer(self):
        global _choices
        print(self.buttons[_choices[0]]._in)
        print(self.buttons[_choices[1]]._in)
        print(self.buttons[_choices[2]]._in)
        print(self.buttons[_choices[3]]._in)

        lock = Lock()
        global ans
        ans = ''
        lock.acquire(True)

        def hooker(pin, val):
            global ans
            
            try:
                for c in _choices:
                    ans = c if self.buttons[c]._in == pin else ans
            finally:
                lock.release()

        self.buttons[_choices[0]].hook(hooker)
        self.buttons[_choices[1]].hook(hooker)
        self.buttons[_choices[2]].hook(hooker)
        self.buttons[_choices[3]].hook(hooker)

        def timeout():
            try:
                return lock.release()
            except:
                print('Lock release fail')
        
        t = Timer(C.RoundTime, timeout)
        t.start()
        lock.acquire(True)
        self._board.clearHooks()
        lock.release()
        
        return ans

# Ask Questions
def AskQuestions(player_count):
    score = C.InitScore
    dbConnect = create_engine(C.DB_URL)
    dbConnection = dbConnect.connect()

    boards_ = [Boards[i] for i in C.BoardStack]
    Players = {}
    b = B = 0
    for c in [chr(i) for i in range(97, 97 + player_count)]:
        Players[c] = Player(boards_[B], (b * 8) + 1)
        if b >= C.BoardPlayerLimit:
            b = 0
            B += 1
        else:
            b += 1

    def getPlayer():
        i = 0
        while True:
            i += 1
            if i >= len(Players.keys()):
                i = 0
            yield Players[list(Players.keys())[i]]
            
    GP = getPlayer()
    print (GP)
             
    while (1):
        # Ask question and verify answer
        query = dbConnection.execute('''SELECT
                        g.rowid,
                        g.QUESTION,
                        g.yellow,
                        g.green,
                        g.red,
                        g.blue,
                        g.correct_answer
                    FROM
                        go_time_trivia AS g
                    WHERE
                        g.has_been_used = 0
                    ORDER BY
                        RANDOM() ASC
                ''')
        #result = {'trivia_question': [dict(zip(tuple(query.keys()), i))
        #                              for i in query.cursor]}
        
        for row in query:
            q = dbConnection.execute('''
            UPDATE go_time_trivia
            SET has_been_used = 1
            WHERE rowid = %s;
            ''' % row['rowid'])

            thisPlayer = next(GP)

            def flash(t):
                thisPlayer.lightAll()
                time.sleep(t)
                thisPlayer.lightAll(False)

            print("rowid: ", row['rowid'])
            print("question: ", row['question'])
            print("yellow: ", row['yellow'])
            print("green: ", row['green'])
            print("red: ", row['red'])
            print("blue: ", row['blue'])
            print("correct_answer: ", row['correct_answer'])
            C.RowID = row['rowid']
            C.Question = row['question']
            C.Ans_Yellow = row['yellow']
            C.Ans_Green = row['green']
            C.Ans_Red = row['red']
            C.Ans_Blue = row['blue']
            C.Ans_Correct = row['correct_answer']

            flash(C.InviteSleep)

            D.setQuestion(row['question'])
            D.setAnswer('red', row['red'])
            D.setAnswer('green', row['green'])
            D.setAnswer('yellow', row['yellow'])
            D.setAnswer('blue', row['blue'])
            D.setRoundTimer(C.RoundTime)
            D.flush()
            D.start()

            # Send question to the board and wait for answer
            ans = thisPlayer.catchAnswer()
            D.setSelected(ans)
            if ans != row['correct_answer']:
                print("Wrong")
                score = score - C.DecScore
                D.doWrong()
            else:
                print("Correct Answer")
                D.setCorrect(ans)
                score = score + C.IncScore
            D.setScore(score)
            D.flush()
            C.Score = score
            
            flash(C.InviteSleep / 2)

            if stopGameEvent.is_set():
                AskQuestions = score
                print("The final score was: %5d" % (score))
                dbConnection.close()
                D.close()
                return score
                break

    dbConnection.close()
    return score

#--------------------------------------------------------------------------------
#- The Quiz Show Game
#--------------------------------------------------------------------------------
score = C.InitScore

# Start Game loop
# Create Question thread
questionThread = None

# Here we start the thread and we wait 330 seconds before the code continues to execute.
@api.route('/', methods=['POST'])
def start():
    player_count = int(request.form['playerCount'])
    C.PlayerCount = player_count
    
    questionThread = Thread(target=AskQuestions, args=[player_count])
    questionThread.daemon = True
    questionThread.start()
    return 'ok'

@api.route('/dump', methods=['GET'])
def get():
    def props(obj):
        pr = {}
        for name in dir(obj):
            value = getattr(obj, name)
            if not name.startswith('_') and not inspect.ismethod(value):
                pr[name] = value
        return pr
    t = props(C)
    return json.dumps(t)

@api.route('/', methods=['GET'])
def delete():
    os.kill(os.getpid(), signal.SIGUSR1)

D.hook('gameover', C.Me_Host)
D.flush()

api.run(host='0.0.0.0')
score = questionThread.join(timeout=630)
if (isinstance(score, int) == False):
    score = score = C.InitScore

# We send a signal that the other thread should stop.
stopGameEvent.set()

print("Hey there! You timed out! The Game is over!")
print("The final score was: %5d" % (score))
