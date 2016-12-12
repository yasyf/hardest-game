import random
from state import ToyGame2DHardState

class Level(object):
  def __init__(self, nenemies):
    self.enemy_phase = {}
    for i in range(nenemies):
      self.enemy_phase[self._rand_loc()] = random.randint(2, 4)

  def _rand_loc(self):
    while True:
      loc = random.randint(0, ToyGame2DHardState.MAX_X), random.randint(0, ToyGame2DHardState.MAX_Y)
      if loc == (0, 0) or loc == (ToyGame2DHardState.MAX_X, ToyGame2DHardState.MAX_Y) or loc in self.enemy_phase:
        continue
      return loc

  @classmethod
  def default(cls):
    return cls(3)
