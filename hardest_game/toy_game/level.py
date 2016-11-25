import random
from state import ToyGameState

class Level(object):
  RANDOM_DEFAULT = True
  DEFAULT_STATIC_LEVEL = (2, 2)

  def __init__(self, enemy_loc, enemy_phase):
    self.enemy_loc = int(enemy_loc)
    self.enemy_phase = int(enemy_phase)

  @classmethod
  def default(cls):
    if cls.RANDOM_DEFAULT:
      return cls(random.randint(1, ToyGameState.MAX_X), 2)
    else:
      return cls(*cls.DEFAULT_STATIC_LEVEL)
