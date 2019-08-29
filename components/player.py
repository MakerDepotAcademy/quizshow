from time import sleep

from itertools import cycle
from questions import CHOICES
from settings import BoardStack, Time
from gpio32.lib import Manager


class Button():

  def __init__(self, board, pin_out, pin_in):
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

  def clearHooks(self):
    self._board.clearHooks()


class Player():
    
  def __init__(self, board, bot, id=None):
    self.buttons = { l: Button(board, i, i + 1) for l, i in zip( CHOICES, range(bot, bot + 8, 2) ) }
    self._board = board
    self._id = id

  def lightAll(self, on=True):
    for b in self.buttons:
      self.buttons[b].light(on)
    self._board.run()

  def flash(self, time):
    self.lightAll()
    sleep(time)
    self.lightAll(False)

  def __getitem__(self, x):
    return self.buttons[x]

  def catchAnswer(self):
    def b(i=None):
      if i != None:
        return self.buttons[CHOICES[i]]._in
      else:
        return [b(i) for i in range(len(CHOICES))]
        
    try:
      ret = self._board.awaitChange(b(), Time().Round_Time)
    except:
      return ''

    for i in range(3):
      if ret == b(i):
        return CHOICES[i]


def assignPlayers(player_count):
  Settings = BoardStack()
  manager = Manager()
  boards = [manager[i] for i in Settings.Board_Stack]
  Players = []

  for i in range(player_count):
    b = boards[i // (player_count-1)]
    s = (i % 5) * 8
    p = Player(b, s, i)
    Players.append(p)

  return Players

def cyclePlayers(players):
  return cycle(players)