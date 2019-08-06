import datetime
from sqlalchemy import create_engine
import time
from threading import Thread, Event

# Event object used to send signals from one thread to another
stopGameEvent = Event()

# Ask Questions
def AskQuestions():
    score = 0
    dbConnect = create_engine('sqlite:///quizShow.db')

    dbConnection = dbConnect.connect()
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
            print("rowid: ", row['rowid'])
            print("question: ", row['question'])
            print("yellow: ", row['yellow'])
            print("green: ", row['green'])
            print("red: ", row['red'])
            print("blue: ", row['blue'])
            print("correct_answer: ", row['correct_answer'])

            # Send question to the board and wait for answer
            ans = input(row['question'])
            if ans != row['correct_answer']:
                print("Wrong")
                score = score - 1
            else:
                print("Correct Answer")
                score = score + 1

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
