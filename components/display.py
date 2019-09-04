from json import dumps
from components.questions import CHOICES
import websocket


class DONOTUSEME(Exception):

    def __init__(self):
        Exception.__init__("Do Not Use Me")

class Display():

    def __init__(self, address):
        self._address = address
        self._payload = dict()
        self.isPaused = False
        self.isRunning = False
        self._ws = websocket.WebSocket()
        self._ws.connect('ws://' + self._address)

    def _getEndpoint(self, endpoint):
        return endpoint

    def _queue(self, endpoint, payload):
        self._payload[endpoint] = payload

    def flush(self):
        print(self._payload)
        self._ws.send(dumps(self._payload))
        self._payload = dict()

    def setQuestion(self, question):
        self._queue('question', question)

    def _getLabel(self, label, edge=None):
        edge = '.' + edge if edge is not None else ''
        return label + edge

    def setAnswer(self, label, answer):
        self._queue(self._getLabel(label), answer)

    def setCorrect(self, label):
        self._queue(self._getLabel(label, 'correct'), '')

    def setSelected(self, label):
        self._queue(self._getLabel(label, 'selected'), '')

    def setScore(self, score):
        self._queue('score', score)

    def setRoundTimer(self, secs):
        self._queue('roundtick', secs)
        self.flush()
    
    def setGameTimer(self, secs):
        self._queue('gametick', secs)
        self.flush()

    def doWrong(self):
        self._queue('wrong', '')

    def playVideo(self, vidpath):
        requests.post(self._getEndpoint('videoplay'), vidpath)

    def playAudio(self, audpath):
        requests.post(self._getEndpoint('audioplay'), audpath)

    def restart(self):
        requests.post(self._getEndpoint('restart'), '')

def displayQuestion(display, question):
    display.setQuestion(question.question)
    for c in CHOICES:
        display.setAnswer(c, question.answers[c])

    display.flush()