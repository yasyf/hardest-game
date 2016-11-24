import hashlib
import numpy as np

class State(object):
  def __init__(self, x, y, coins, level, deaths, moves):
    self.x = x
    self.y = y
    self.coins = coins
    self.level = level
    self.deaths = deaths
    self.moves = moves

  @staticmethod
  def id_for_moves(moves):
    return hashlib.md5(''.join(map(lambda x: str(x.value), moves))).hexdigest()

  def is_start(self):
    return self.level.start.contains(self)

  def is_end(self):
    return self.level.end.contains(self)

  def id(self):
    return self.id_for_moves(self.moves)

  def is_death(self):
    return self.deaths > 0

  def is_win(self):
    return self.level.coins == self.coins and self.is_end()

  def log_distance_to_end(self):
    difference = (self.level.end.x - self.x, self.level.end.y - self.y)
    return np.log(np.linalg.norm(difference))
