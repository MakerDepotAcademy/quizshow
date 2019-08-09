import requests
from json import dumps

class Display():

    def __init__(self, address):
        self._address = address

    def _getEndpoint(self, endpoint):
        return 'http://%s/%s' % (self._address, endpoint)

    def _post(self, endpoint, payload):
        print('%s, %s, %s' % (endpoint, payload, dumps(payload)))
        return requests.post(self._getEndpoint(endpoint), data=str(payload), headers={'Content-Type': 'application/x-www-form-urlencoded'})

    def setQuestion(self, question):
        self._post('question', question)

    def setAnswer(self, label, answer):
        self._post('answer/%s' % label, answer)

    def setCorrect(self, label):
        self._post('answer/%s/correct' % label, '')

    def setScore(self, score):
        self._post('score', score)

    def addScore(self, add):
        self._post('score/inc', add)

    def subScore(self, sub):
        self._post('score/dec', sub)

    def getScore(self):
        rsp = requests.get(self._getEndpoint('score'))
        return int(rsp.content)

    def start(self):
        self._post('start', '3')

    def setRoundTimer(self, secs):
        self._post('timer/round', secs)
    
    def setGameTimer(self, secs):
        self._post('timer/game', secs)