import requests
from json import dumps
from socket import gethostname

class DoNotUseMe(Exception):
    def __init__(self):
        print('DO NOT USE ME')

class Display():

    def __init__(self, address):
        self._address = address
        self._payload = dict()
        self.isPaused = False
        self.isRunning = False

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
        raise DoNotUseMe()

    def subScore(self, sub):
        raise DoNotUseMe()

    def getScore(self):
        raise DoNotUseMe()

    def start(self):
        self.isRunning = True
        requests.post(self._getEndpoint('start'))

    def setRoundTimer(self, secs):
        self._post('timer/round', secs)
    
    def setGameTimer(self, secs):
        self._post('timer/game', secs)

    def doWrong(self):
        self._post('wrong', '')

    def hook(self, event, me):
        # rsp = requests.post(self._getEndpoint('subscribe/%s' % event), data='http://%s:5000/' % gethostname())
        self._post('subscribe', {
            'event': 'gameover',
            'uri': 'http://%s/' % me,
            'method': 'GET'
        })

    def restart(self):
        requests.post(self._getEndpoint('restart'))

    def close(self):
        requests.delete(self._getEndpoint(''))

    def pause(self):
        self.isPaused = not self.isPaused
        requests.post(self._getEndpoint('pause'))

    def playVideo(self, vidpath):
        requests.post(self._getEndpoint('videoplay'), vidpath)

    def playAudio(self, audpath):
        requests.post(self._getEndpoint('audioplay'), audpath)