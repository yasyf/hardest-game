from ..toy_game_2d.state import ToyGame2DState, NSQUARES
import numpy as np

class ToyGame2DHardState(ToyGame2DState):
  def enemy_shown(self):
    return True

  def enemy_at_loc(self, pos):
    return pos in self.level.enemy_phase and self.frame % (2*self.level.enemy_phase[pos]) >= self.level.enemy_phase[pos]

  def _draw_enemy(self, d):
    for loc in self.level.enemy_phase:
      if self.enemy_at_loc(loc):
        d.rectangle(self._bounding_box(loc[0], loc[1], 5, 5), fill='blue', outline='blue')

  def feature_vector(self):
    x = np.zeros((NSQUARES, NSQUARES))
    x[self.y, self.x] = 1
    for loc in self.level.enemy_phase:
      if self.enemy_at_loc(loc):
        x[loc[1], loc[0]] += 1
        x[loc[1], loc[0]] *= -1
    return x.flatten()
