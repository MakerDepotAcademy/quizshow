import unittest
import lib

def forAllBoards(fn):
  def wrapper(self):
    for id in self.manager:
      self.thisBoard = self.manager[id]
      fn(self)

  return wrapper

def forAllPins(fn):
  def wrapper(self):
    for i in range(self.thisBoard._queuelen):
      self.thisPin = i
      fn(self)
    self.thisBoard.run()
    self.assertTrue(True)

  return wrapper

class Lib_Test(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    cls.manager = lib.Manager()

  @classmethod
  def tearDownClass(cls):
    cls.manager.closeall()

  @forAllBoards
  def test_tryAllPins(self):
    for id in self.manager:
      m = self.manager[id]
      for i in range(31):
        m.turnOn(i)
        m.turnOff(i)
        m.setInput(i, True)
        m.setInput(i, False)

    self.assertTrue(True)

  @forAllBoards
  @forAllPins
  def test_turnAllOn(self):
    self.thisBoard.turnOn(self.thisPin)

  @forAllBoards
  @forAllPins
  def test_turnAllOff(self):
    self.thisBoard.turnOff(self.thisPin)

  @forAllBoards
  @forAllPins
  def test_setAllInputs(self):
    self.thisBoard.setInput(self.thisPin)

  @forAllBoards
  @forAllPins
  def test_setAllInputsInverse(self):
    self.thisBoard.setInput(self.thisPin, True)

  def test_getLocation(self):
    for id in self.manager:
      m = self.manager[id]
      l = m.getLocation()
      self.assertTrue(l)

  def test_getPorts(self):
    for id in self.manager:
      m = self.manager[id]
      l = m.getPorts()
      self.assertTrue(l)

  def test_getIDs(self):
    for id in self.manager:
      m = self.manager[id]
      l = m.getID()
      self.assertTrue(l)

  def test_interupts(self):
    def hook(pin, val):
      self.assertTrue(True)

    for id in self.manager:
      m = self.manager[id]
      m.onChange(hook) 


if __name__ == '__main__':
  unittest.main()