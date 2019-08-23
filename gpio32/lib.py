import serial
from pathlib import Path
from threading import Thread, Lock
import re

class Board():
  
  def __init__(self, port, qu=32):
    self._ser = serial.Serial(str(port), 2000000, timeout=1)
    self._ser.flushInput()
    self._ser.flushOutput()
    self._hooks = []
    self.queue = ['x'] * qu
    self._queuelen = qu
    self._eventThread = Thread(target=self._eventLoop)
    self._eventAlive = False
    self._eventLock = Lock()

  def close(self):
    self._ser.close()

  def _eventLoop(self):
    last = ''
    while True:
      self._eventLock.acquire(True)
      line = self._ser.readline()
      self._eventLock.release()

      if len(line) == 0 or last == line:
        continue
      
      for i, (c, l) in enumerate(zip(line, last)):
        if c != l:
          for hook, pin in self._hooks:
            if pin == -1 or pin == i + 1:
              hook(pin, c == '1')

      last = line

  def run(self):
    t = ''.join(self.queue) + '\n'
    self._ser.write(t.encode())
    self.queue = ['x'] * self._queuelen

  def _setpin(self, pin, val):
    self.queue[pin - 1] = val

  def _prompt(self, p):
    self.run()
    self._eventLock.acquire(True)
    self._ser.write(p)
    r = self._ser.readline().decode()
    self._eventLock.release()
    return r.strip()

  def turnOn(self, pin):
    self._setpin(pin, '1')

  def turnOff(self, pin):
    self._setpin(pin, '0')

  def setInput(self, pin, inverse=False):
    self._setpin(pin, 'u' if inverse else 'i')

  def unsetInput(self, pin, inverse=False):
    self._setpin(pin, 'U' if inverse else 'I')

  def setInterrupt(self, pin, enabled=True):
    self._setpin(pin, 'e' if enabled else 'd')

  def getID(self):
    return self._prompt('?')
    
  def getLocation(self):
    return self._prompt('l')
  
  def getPorts(self):
    return self._prompt('r')

  def onChange(self, hook, pin=-1):
    self._hooks.append((hook, pin))
    
    if pin == -1:
      self.queue = 'e' * self._queuelen
    else:
      self.queue[pin - 1] = 'e'

    self.run()

    if not self._eventAlive:
      self._eventThread.start()
      self._eventAlive = True

  def clearHooks(self):
    self._hooks = []
    self.queue = 'd' * self._queuelen
    self.run()

  def clearHook(self, pin):
    for i, ent in enumerate(self._hooks):
      if ent[1] == pin:
        del self._hooks[i]
        self.queue[pin - 1] == 'd'

    self.run()

  def awaitChange(self, pins, timeout):
    def m(l):
      return re.match(r'[01]', l)

    def readline(t=timeout):
      l = ''
      while t > 0:
        l = self._ser.readline()
        if l == '':
          t -= 1
        else:
          return l
      raise Exception('Timeout')

    
    for p in pins:
      self.setInput(p)

    self.run()
    last = ''
    while not last:
      last = readline()
      last = '' if not m(last) else last
      
    while True:
      l = readline()
      if l == last:
        continue
      
      if m(l): 
        for p in pins:
          p -= 1
          if l[p] != last[p]:
            return p + 1

        last = l

class Manager():
  
  def __init__(self):
    # ls /dev/ttyACM*
    self._boards = {}
    for acm in Path('/dev').glob('ttyACM*'):
      b = None
      try:
        b = Board(acm)
        i = str(b.getID())
        if not re.search(r'[a-zA-Z0-9]+', i):
          raise Exception('isnot mine')
        self._boards[i] = b
      except Exception as e:
        print(e)
        b.close()

  def __getitem__(self, i):
    return self.getBoardByID(i)

  def __iter__(self):
    return iter(self._boards)

  def getBoardByID(self, i):
    return self._boards[i]

  def closeall(self):
    for k in self._boards:
      self._boards[k].close()