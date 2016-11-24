import numpy as np
from ..shared.state_base import StateBase

class HardestGameState(StateBase):
  def __init__(self, x, y, coins, level, deaths, moves):
    super(HardestGameState, self).__init__(moves)

    self.x = x
    self.y = y
    self.coins = coins
    self.level = level
    self.deaths = deaths

  def is_start(self):
    return self.level.start.contains(self)

  def is_end(self):
    return self.level.end.contains(self)

  def is_death(self):
    return self.deaths > 0

  def is_win(self):
    return self.level.coins == self.coins and self.is_end()

  def log_distance_to_end(self):
    difference = (self.level.end.x - self.x, self.level.end.y - self.y)
    return np.log(np.linalg.norm(difference))
