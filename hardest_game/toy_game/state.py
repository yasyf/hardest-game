from ..shared.state_base import StateBase
from ..shared.util import WHITE, BLACK
from PIL import Image, ImageDraw
import numpy as np

NSQUARES = 4

class ToyGameState(StateBase):
  MAX_X = NSQUARES - 1
  WIDTH = 80
  HEIGHT = 20
  IMAGE_DIMS = (WIDTH, HEIGHT)

  def __init__(self, x, frame, alive, level, moves):
    super(ToyGameState, self).__init__(moves)

    self.x = x
    self.frame = frame
    self.alive = alive
    self.level = level

  def is_win(self):
    return self.alive and self.x == self.MAX_X

  def enemy_shown(self):
    return self.frame % (2*self.level.enemy_phase) >= self.level.enemy_phase

  @classmethod
  def _bounding_box(cls, x, width, height):
    x_center = (cls.WIDTH / NSQUARES) * (x + 0.5)
    y_center = cls.HEIGHT / 2
    return [(x_center - width/2, y_center - height/2), (x_center + width/2, y_center + height/2)]

  @classmethod
  def _new_draw(cls):
    img = Image.new('RGB', cls.IMAGE_DIMS, (WHITE,) * 3)
    d = ImageDraw.Draw(img)
    return img, d

  @classmethod
  def _draw_rectangle(cls, d):
    d.rectangle([(0, 0), (cls.WIDTH - 1, cls.HEIGHT - 1)], outline=BLACK)

  @classmethod
  def _draw_lines(cls, d):
    for i in range(NSQUARES):
      d.line([((cls.WIDTH / NSQUARES) * i, 0), ((cls.WIDTH / NSQUARES) * i, cls.HEIGHT - 1)], fill=BLACK)

  def _draw_player(self, d):
    d.rectangle(self._bounding_box(self.x, 10, 10), fill='red', outline='red')

  def _draw_enemy(self, d):
    d.rectangle(self._bounding_box(self.level.enemy_loc, 5, 5), fill='blue', outline='blue')

  def draw(self):
    img, d = self._new_draw()
    self._draw_rectangle(d)
    self._draw_lines(d)
    self._draw_player(d)
    if self.enemy_shown():
      self._draw_enemy(d)
    return img

  def distance_to_end(self):
    return self.MAX_X - self.x

  def feature_vector(self):
    x = np.zeros(NSQUARES)
    x[self.x] = 1
    if self.enemy_shown():
      x[self.level.enemy_loc] = (x[self.level.enemy_loc] + 1) * -1
    return x
