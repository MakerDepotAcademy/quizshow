import requests

class Display():

    def __init__(self, address):
        self._address = address

    def _getEndpoint(self, endpoint):
        return 'http://%s/%s' % (self._address, endpoint)

    def _post(self, endpoint, payload):
        return requests.post(_getEndpoint(endpoint), data=payload)

    def setQuestion(self, question):
        self._post('/question', question)

    def setAnswer(self, label, answer):
        self._post('/answer/%s' % label, answer)

    def setCorrect(self, label):
        self._post('/answer/%s/correct' % label, '')

    def setScore(self, score):
        self._post('/score', score)

    def addScore(self, add):
        self._post('/score/inc', add)

    def subScore(self, sub):
        self._post('/score/dec', sub)

    def getScore(self):
        rsp = requests.get(self._getEndpoint('/score'))
        return int(rsp.content)

    def start(self):
        self._post('/start')