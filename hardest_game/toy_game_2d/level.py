import random
from state import ToyGame2DState

class Level(object):
  RANDOM_DEFAULT = True
  DEFAULT_STATIC_LEVEL = ((1, 1), 2)

  def __init__(self, enemy_loc, enemy_phase):
    self.enemy_loc = tuple(map(int, enemy_loc))
    self.enemy_phase = int(enemy_phase)

  @classmethod
  def default(cls):
    if cls.RANDOM_DEFAULT:
      return cls((random.randint(1, ToyGame2DState.MAX_X), random.randint(1, ToyGame2DState.MAX_Y)), 2)
    else:
      return cls(*cls.DEFAULT_STATIC_LEVEL)
