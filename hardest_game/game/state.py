import hashlib
import numpy as np

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

  def is_dead(self):
    return self.deaths > 0

  def is_win(self):
    return self.level.coins == self.coins and self.level.end.contains(self)

  def log_distance_to_end(self):
    difference = (self.level.end.x - self.x, self.level.end.y - self.y)
    np.log(np.linalg.norm(difference))
