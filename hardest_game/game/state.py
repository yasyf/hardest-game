import hashlib

class State(object):
  def __init__(self, x, y, coins, level, deaths, history):
    self.x = x
    self.y = y
    self.coins = coins
    self.level = level
    self.deaths = deaths
    self.history = history

  @staticmethod
  def id_for_history(history):
    return hashlib.md5(''.join(map(lambda x: str(x.value), history))).hexdigest()

  def id(self):
    return self.id_for_history(self.history)
