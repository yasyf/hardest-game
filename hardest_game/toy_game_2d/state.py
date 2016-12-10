from ..toy_game.state import ToyGameState, NSQUARES
from ..shared.util import BLACK
import numpy as np


class ToyGame2DState(ToyGameState):
  MAX_Y = NSQUARES - 1
  WIDTH = 80
  HEIGHT = 80
  IMAGE_DIMS = (WIDTH, HEIGHT)

  def __init__(self, x, y, frame, alive, level, moves):
    super(ToyGame2DState, self).__init__(x, frame, alive, level, moves)

    self.y = y

  def is_win(self):
    return super(ToyGame2DState, self).is_win() and self.y == self.MAX_Y

  @classmethod
  def _bounding_box(cls, x, y, width, height):
    x_center = (cls.WIDTH / NSQUARES) * (x + 0.5)
    y_center = (cls.HEIGHT / NSQUARES) * (y + 0.5)
    return [(x_center - width/2, y_center - height/2), (x_center + width/2, y_center + height/2)]

  @classmethod
  def _draw_lines(cls, d):
    for i in range(NSQUARES):
      d.line([(0, (cls.HEIGHT / NSQUARES) * i), (cls.WIDTH - 1, (cls.HEIGHT / NSQUARES) * i)], fill=BLACK)
      d.line([((cls.WIDTH / NSQUARES) * i, 0), ((cls.WIDTH / NSQUARES) * i, cls.HEIGHT - 1)], fill=BLACK)

  def _draw_player(self, d):
    d.rectangle(self._bounding_box(self.x, self.y, 10, 10), fill='red', outline='red')

  def _draw_enemy(self, d):
    d.rectangle(self._bounding_box(self.level.enemy_loc[0], self.level.enemy_loc[1], 5, 5), fill='blue', outline='blue')

  def distance_to_end(self):
    return (self.MAX_X - self.x) + (self.MAX_Y - self.y)

  def feature_vector(self):
    x = np.zeros((NSQUARES, NSQUARES))
    x[self.y, self.x] = 1
    if self.enemy_shown():
      x[self.level.enemy_loc[1], self.level.enemy_loc[0]] += 1
      x[self.level.enemy_loc[1], self.level.enemy_loc[0]] *= -1
    return x.flatten()
