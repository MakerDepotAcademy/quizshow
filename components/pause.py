from threading import Lock

class Pause():

  def __init__(self, hook):
    self._lock = Lock()
    self._hook = hook

  def block_if_paused(self):
    self._lock.acquire(True)
    self._lock.release()

  def pause(self):
    if self._lock.isLocked():
      self._lock.release()
      self._hook(False)
    else:
      self._hook(True)
      self._lock.acquire(True)