import unittest
import lib

class Lib_Test(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    cls.manager = lib.Manager()

  @classmethod
  def tearDownClass(cls):
    cls.manager.closeall()

  def test_tryAllPins(self):
    for id in self.manager:
      m = self.manager[id]
      for i in range(31):
        m.turnOn(i)
        m.turnOff(i)
        m.setInput(i, True)
        m.setInput(i, False)

    self.assertTrue(True)

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