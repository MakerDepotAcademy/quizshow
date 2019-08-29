from sqlalchemy import create_engine
from settings import Database

CHOICES = ['red', 'green', 'blue', 'yellow']

class Question():

  def __init__(self, **kwargs):
    self.question = kwargs['question']
    self.id = kwargs['id']
    self.correct = kwargs['correct']
    self.answers = {}
    for c in CHOICES:
      self.answers[c] = kwargs[c]

  def checkAnswer(self, ans):
    return ans == self.correct

def getQuestions():
  dbConnect = create_engine(Database().URL)
  dbConnection = dbConnect.connect()
  dbConnection.execute('''
                        UPDATE go_time_trivia
                        SET has_been_used = 0
                        ''')
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

  for r in query:
    dbConnection.execute('''
                        UPDATE go_time_trivia
                        SET has_been_used = 1
                        WHERE rowid = %s;
                        ''' % r['rowid'])
    yield Question(id=r['rowid'], red=r['red'], blue=r['blue'], green=r['green'], yellow=r['yellow'], correct=r['correct_answer'], question=r['question'])
