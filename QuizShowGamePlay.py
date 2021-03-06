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
from itertools import cycle
import check_conf as boardconfig

# Event object used to send signals from one thread to another
stopGameEvent = Event()
Boards = Manager()
api = Flask(__name__)
global PAUSE
PAUSE = Lock()

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
        self.Video = sec['PREAMBLE_VID']

C = Config()

D = Display(C.Display_Host)
D.restart()
D.setGameTimer(C.GameTime)

class Button():

    def __init__(self, board, pin_out, pin_in):
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
    
    def __init__(self, board, buttonsDict):
        global _choices
        # self.buttons = { l: Button(board, i, i + 1) for l, i in zip( _choices, range(bot, bot + 8, 2) ) }
        for c in _choices:
            self.buttons[c] = Button(board, buttonsDict[c]['out'], buttonsDict[c]['in'])

    def lightAll(self, on=True):
        for b in self.buttons:
            self.buttons[b].light(on)
        self._board.run()

    def __getitem__(self, x):
        return self.buttons[x]

    def catchAnswer(self):
        global _choices
        def b(i=None):
            if i != None:
                return self.buttons[_choices[i]]._in
            else:
                return [b(i) for i in range(len(_choices))]
        
        print(b())
        try:
            ret = self._board.awaitChange(b(), C.RoundTime)
        except:
            return ''

        for i in range(3):
            if ret == b(i):
                return _choices[i]

def blockIfPaused():
    global PAUSE
    d = PAUSE.locked()
    if d:
        D.pause()
    PAUSE.acquire(True)
    PAUSE.release()
    if d:
        D.start()

# Ask Questions
def AskQuestions(player_count):
    D.playVideo(C.Video)

    score = C.InitScore
    dbConnect = create_engine(C.DB_URL)
    dbConnection = dbConnect.connect()

    # boards_ = [Boards[int(i)] for i in C.BoardStack]
    # print(dir(boards_))
    Players = {}
    # b = B = 0
    # for c in [chr(i) for i in range(97, 97 + player_count)]:
    #     Players[c] = Player(boards_[B], (b * 8))
    #     if b >= C.BoardPlayerLimit:
    #         b = 0
    #         B += 1
    #     else:
    #         b += 1

    
    if boardconfig.check():
        conf = boardconfig.load()    
        for key, value in conf.items():
            Player[key] = Player(Boards[value['board_id']], value['buttons'])

                        
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
        
        GP = cycle(Players.values()) 
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

            blockIfPaused()
            flash(C.InviteSleep)

            D.setQuestion(row['question'])
            D.setAnswer('red', row['red'])
            D.setAnswer('green', row['green'])
            D.setAnswer('yellow', row['yellow'])
            D.setAnswer('blue', row['blue'])
            D.setRoundTimer(C.RoundTime)
            D.flush()
            D.start()

            blockIfPaused()
            # Send question to the board and wait for answer
            ans = thisPlayer.catchAnswer()
            if ans != row['correct_answer']:
                if ans != '':
                    D.setSelected(ans)
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
def gameTimeout():
    # This will nuke threads too, thanks brad
    i = C.GameTime
    while i > 0:
        blockIfPaused()
        time.sleep(1)
        i -= 1
        if i == 0:
            os.kill(os.getpid(), signal.SIGUSR1)
            return

gameTimer = Thread(target=gameTimeout)

# Here we start the thread and we wait 330 seconds before the code continues to execute.
@api.route('/', methods=['POST'])
def start():
    player_count = int(request.form['playerCount'])
    C.PlayerCount = player_count
    
    questionThread = Thread(target=AskQuestions, args=[player_count])
    questionThread.daemon = True
    questionThread.start()
    gameTimer.start()
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

@api.route('/pause', methods=['GET'])
def handlepause():
    global PAUSE
    if PAUSE.locked():
        PAUSE.release()
    else:
        PAUSE.acquire(True)
        
    return 'ok'

D.flush()
api.run(host='0.0.0.0')
score = questionThread.join(timeout=C.GameTime)
if (isinstance(score, int) == False):
    score = score = C.InitScore

# We send a signal that the other thread should stop.
stopGameEvent.set()

print("Hey there! You timed out! The Game is over!")
print("The final score was: %5d" % (score))
