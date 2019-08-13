import serial
from pathlib import Path
import threading
import re

class Board():
  
  def __init__(self, port):
    self._ser = serial.Serial(str(port), 2000000, timeout=1)
    self._ser.flushInput()
    self._ser.flushOutput()
    self._hooks = []

    self._eventThread = threading.Thread(target=self._eventLoop)
    self._eventAlive = False

  def close(self):
    self._ser.close()

  def _eventLoop(self):
    last = ''
    while True:
      line = self._ser.readline()

      if len(line) == 0:
        continue

      if len(line) != 34:
        self._ser.seek(len(line), 2)
        continue

      if last == line:
        continue
      
      for i, (c, l) in enumerate(zip(line, last)):
        if c != l:
          for hook, pin in self._hooks:
            if pin == -1 or pin == i + 1:
              hook(pin, c == '1')

      last = line

  def _write(self, l):
    t = '%s\n' % l
    self._ser.write(t.encode())

  def _setpin(self, pin, postfix):
    self._write('s%s%s' % (pin, postfix))

  def _prompt(self, p):
    self._write(p)
    r = self._ser.readline().decode()
    return r.strip()

  def turnOn(self, pin):
    self._setpin(pin, '+')

  def turnOff(self, pin):
    self._setpin(pin, '-')

  def setInput(self, pin, inverse=False):
    self._setpin(pin, 'u' if inverse else 'i')

  def getID(self):
    return self._prompt('?')
    
  def getLocation(self):
    return self._prompt('l')
  
  def getPorts(self):
    return self._prompt('r')

  def onChange(self, hook, pin=-1):
    self._hooks.append((hook, pin))

    if not self._eventAlive:
      self._eventThread.start()
      self._eventAlive = True

  def clearHooks(self):
    self._hooks = []

class Manager():
  
  def __init__(self):
    # ls /dev/ttyACM*
    self._boards = {}
    for acm in Path('/dev').glob('ttyACM*'):
      b = None
      try:
        b = Board(acm)
        i = b.getID()
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