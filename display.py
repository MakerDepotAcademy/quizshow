import requests
from json import dumps
from socket import gethostname

class Display():

    def __init__(self, address):
        self._address = address
        self._payload = dict()

    def _getEndpoint(self, endpoint):
        return 'http://%s/%s' % (self._address, endpoint)

    def _post(self, endpoint, payload):
        # print('%s, %s, %s' % (endpoint, payload, dumps(payload)))
        # return requests.post(self._getEndpoint(endpoint), data=str(payload), headers={'Content-Type': 'application/x-www-form-urlencoded'})
        self._payload[endpoint] = payload

    def flush(self):
        p = self._payload
        print(p)
        self._payload = dict()
        return requests.post(self._getEndpoint(''), data=dumps(p), headers={'Content-Type': 'application/json'})


    def setQuestion(self, question):
        self._post('question', question)

    def _getLabel(self, label, edge=None):
        edge = '-' + edge if edge is not None else ''
        return '%s%s' % (label, edge)

    def setAnswer(self, label, answer):
        self._post(self._getLabel(label), answer)

    def setCorrect(self, label):
        self._post(self._getLabel(label, 'correct'), '')

    def setSelected(self, label):
        self._post(self._getLabel(label, 'selected'), '')

    def setScore(self, score):
        self._post('score', score)

    def addScore(self, add):
        raise Exception('DO NOT USE ME')

    def subScore(self, sub):
        raise Exception('DO NOT USE ME')

    def getScore(self):
        raise Exception('DO NOT USE ME')

    def start(self):
        requests.post(self._getEndpoint('start'))

    def setRoundTimer(self, secs):
        self._post('timer/round', secs)
    
    def setGameTimer(self, secs):
        self._post('timer/game', secs)

    def doWrong(self):
        self._post('wrong', '')

    def hook(self, event):
        rsp = requests.post(self._getEndpoint('subscribe/%s' % event), data='http://%s:5000/' % gethostname())

    def restart(self):
        requests.post(self._getEndpoint('restart'))

    def close(self):
        requests.delete(self._getEndpoint(''))