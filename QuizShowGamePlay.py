import datetime
from sqlalchemy import create_engine
import time
from threading import Thread, Event, Lock
from display import Display
from gpio32.lib import Manager
from flask import Flask, request



# Event object used to send signals from one thread to another
stopGameEvent = Event()
D = Display('localhost:8080')
Boards = Manager()
api = Flask(__name__)

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

class Player():

    def __init__(self, board, bot):
        self.buttons = { l: Button(board, i, i + 1) for l, i in zip( 'abcd', range(bot, bot + 8, 2) ) }
        self._board = board

    def lightAll(self, on=True):
        for b in self.buttons:
            self.buttons[b].light(on)

    def __getitem__(self, x):
        return self.buttons[x]

    def catchAnswer(self):
        print(self.buttons['a']._in)
        print(self.buttons['b']._in)
        print(self.buttons['c']._in)
        print(self.buttons['d']._in)

        lock = Lock()
        global ans
        ans = ''
        lock.acquire(True)

        def hooker(pin, val):
            global ans
            
            try:
                for c in 'abcd':
                    ans = c if self.buttons[c]._in == pin else ans
            finally:
                lock.release()

        self.buttons['a'].hook(hooker)
        self.buttons['b'].hook(hooker)
        self.buttons['c'].hook(hooker)
        self.buttons['d'].hook(hooker)
        

        lock.acquire(True)
        self.buttons['a'].clearHooks()
        lock.release()
        
        return ans

# Ask Questions
def AskQuestions(player_count):
    score = 0
    dbConnect = create_engine('sqlite:///quizShow.db')
    dbConnection = dbConnect.connect()

    boards_ = [Boards['65535']]
    Players = {}
    b = B = 0
    for c in [chr(i) for i in range(97, 97 + player_count)]:
        Players[c] = Player(boards_[B], (b * 8) + 1)
        if b > 2:
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
            yield Players[Players.keys()[i]]
            
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
            thisPlayer = next(GP)

            print("rowid: ", row['rowid'])
            print("question: ", row['question'])
            print("yellow: ", row['yellow'])
            print("green: ", row['green'])
            print("red: ", row['red'])
            print("blue: ", row['blue'])
            print("correct_answer: ", row['correct_answer'])

            thisPlayer.lightAll()
            # time.sleep(3)
            thisPlayer.lightAll(False)

            D.setQuestion(row['question'])
            D.setAnswer('a', row['red'])
            D.setAnswer('b', row['green'])
            D.setAnswer('c', row['yellow'])
            D.setAnswer('d', row['blue'])
            
            D.start()

            # Send question to the board and wait for answer
            print ("oh ok im here")
            ans = thisPlayer.catchAnswer()
            if ans != row['correct_answer']:
                print("Wrong")
                score = score - 1
            else:
                print("Correct Answer")
                D.setCorrect(ans)
                score = score + 1
            D.setScore(score)

            if stopGameEvent.is_set():
                AskQuestions = score
                print("The final score was: %5d" % (score))
                dbConnection.close()
                return score
                break

    dbConnection.close()
    return score

#--------------------------------------------------------------------------------
#- The Quiz Show Game
#--------------------------------------------------------------------------------
score = 0

# Start Game loop
# Create Question thread
questionThread = None

# Here we start the thread and we wait 330 seconds before the code continues to execute.
@api.route('/')
def start():
    player_count = int(request.form['playerCount'])
    
    questionThread = Thread(target=AskQuestions, args=[player_count])
    questionThread.start()
    return 'ok'

api.run()
score = questionThread.join(timeout=630)
if (isinstance(score, int) == False):
    score = 0

# We send a signal that the other thread should stop.
stopGameEvent.set()

print("Hey there! You timed out! The Game is over!")
print("The final score was: %5d" % (score))
