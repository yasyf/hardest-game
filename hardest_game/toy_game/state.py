from ..shared.state_base import StateBase
from ..shared.util import WHITE, BLACK
from PIL import Image, ImageDraw

WIDTH = 80
HEIGHT = 20
NSQUARES = 4

class ToyGameState(StateBase):
  MAX_X = NSQUARES - 1
  IMAGE_DIMS = (WIDTH, HEIGHT)

  def __init__(self, x, alive, level, moves):
    super(ToyGameState, self).__init__(moves)

    self._x = int(x)
    self.alive = alive
    self.level = level

  @property
  def x(self):
    return self._x

  @x.setter
  def x(self, new_x):
    new_x = int(new_x)
    if new_x < 0:
      self._x = 0
    elif new_x > self.MAX_X:
      self._x = self.MAX_X
    else:
      self._x = new_x

  def is_win(self):
    return self.alive and self.x == self.MAX_X

  @staticmethod
  def _bounding_box(x, width, height):
    x_center = (WIDTH / NSQUARES) * (x + 0.5)
    y_center = HEIGHT / 2
    return [(x_center - width/2, y_center - height/2), (x_center + width/2, y_center + height/2)]

  def draw(self, frame):
    img = Image.new('RGB', self.__class__.IMAGE_DIMS, (WHITE,) * 3)
    d = ImageDraw.Draw(img)
    d.rectangle([(0, 0), (WIDTH - 1, HEIGHT - 1)], outline=BLACK)
    for i in range(NSQUARES):
      d.line([((WIDTH / NSQUARES) * i, 0), ((WIDTH / NSQUARES) * i, HEIGHT - 1)], fill=BLACK)
    d.rectangle(self._bounding_box(self.x, 10, 10), fill='red', outline='red')
    if frame % self.level.enemy_phase == 0:
      d.rectangle(self._bounding_box(self.level.enemy_loc, 5, 5), fill='blue', outline='blue')
    return img
