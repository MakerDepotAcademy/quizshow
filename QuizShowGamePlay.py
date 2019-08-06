import datetime
from sqlalchemy import create_engine
import time
from threading import Thread, Event
from display import Display
from gpio32.lib import Manager

# Event object used to send signals from one thread to another
stopGameEvent = Event()

D = Display('localhost:8080')
Boards = Manager()

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

class Player():

    def __init__(self, board, bot, top):
        if (top - bot) / 2 != 4:
            raise Exception('Range must be 8 pins long')

        self.buttons = { l: Button(board, i, i + 1) for l, i in zip( ['a', 'b', 'c', 'd'], range(bot, top, 2) ) }
        self._board = board

    def lightAll(self, on=True):
        for b in self.buttons:
            self.buttons[b].light(on)

    def __getitem__(self, x):
        return self.buttons[x]

    def catchAnswer(self):
        ans = ''
        def a(pin, val):
            ans = 'a'
        def b(pin, val):
            ans = 'b'
        def c(pin, val):
            ans = 'c'
        def d(pin, val):
            ans = 'd'

        self.buttons['a'].hook(a)
        self.buttons['b'].hook(b)
        self.buttons['c'].hook(c)
        self.buttons['d'].hook(d)

        self._board._eventThread.join()
        return ans

Players = {
    'a': Player(Boards['65535'], 0, 8),
    'b': Player(Boards['65535'], 9, 18),
    'c': Player(Boards['65535'], 18, 27) # ,
    # 'd': Player(Boards['1'], 0, 8),
    # 'e': Player(Boards['1'], 9, 18)
}

# Ask Questions
def AskQuestions():
    score = 0
    dbConnect = create_engine('sqlite:///quizShow.db')

    dbConnection = dbConnect.connect()

    def getPlayer():
        i = 0
        while True:
            i += 1
            if i > len(Players.keys()):
                i = 0
            yield Players[Players.keys()[i]]
            
    GP = getPlayer()
             
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
            time.sleep(3)
            thisPlayer.lightAll(False)

            D.setQuestion(row['question'])
            D.setAnswer('a', row['red'])
            D.setAnswer('b', row['green'])
            D.setAnswer('c', row['yellow'])
            D.setAnswer('d', row['blue'])
            
            D.start()

            # Send question to the board and wait for answer
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
questionThread = Thread(target=AskQuestions)

# Here we start the thread and we wait 330 seconds before the code continues to execute.
questionThread.start()
score = questionThread.join(timeout=330)
if (isinstance(score, int) == False):
    score = 0

# We send a signal that the other thread should stop.
stopGameEvent.set()

print("Hey there! You timed out! The Game is over!")
print("The final score was: %5d" % (score))
