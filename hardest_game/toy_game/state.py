from ..shared.state_base import StateBase
from ..shared.util import WHITE, BLACK
from PIL import Image, ImageDraw
import numpy as np

WIDTH = 80
HEIGHT = 20
NSQUARES = 4

class ToyGameState(StateBase):
  MAX_X = NSQUARES - 1
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
    return self.frame % self.level.enemy_phase == 0

  @staticmethod
  def _bounding_box(x, width, height):
    x_center = (WIDTH / NSQUARES) * (x + 0.5)
    y_center = HEIGHT / 2
    return [(x_center - width/2, y_center - height/2), (x_center + width/2, y_center + height/2)]

  def draw(self):
    img = Image.new('RGB', self.__class__.IMAGE_DIMS, (WHITE,) * 3)
    d = ImageDraw.Draw(img)
    d.rectangle([(0, 0), (WIDTH - 1, HEIGHT - 1)], outline=BLACK)
    for i in range(NSQUARES):
      d.line([((WIDTH / NSQUARES) * i, 0), ((WIDTH / NSQUARES) * i, HEIGHT - 1)], fill=BLACK)
    d.rectangle(self._bounding_box(self.x, 10, 10), fill='red', outline='red')
    if self.enemy_shown():
      d.rectangle(self._bounding_box(self.level.enemy_loc, 5, 5), fill='blue', outline='blue')
    return img

  def distance_to_end(self):
    return self.MAX_X - self.x

  def feature_vector(self):
    x = np.zeros(NSQUARES)
    x[self.x] = 1
    if self.enemy_shown():
      x[self.level.enemy_loc] = (x[self.level.enemy_loc] + 1) * -1
    return x
