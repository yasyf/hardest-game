from pickleable import Pickleable
import matplotlib.pyplot as plt
from scipy.misc import imresize

LARGE_NUMBER = 1000
BLACK = 0
WHITE = 255
BACKGROUND = [180, 181, 254]
BOARDER = [124, 124, 175]
BLUE_TILE = [230, 230, 255]
WHITE_TILE = [247, 247, 255]

class Sample(Pickleable):
  def __init__(self, state, image):
    self.state = state
    self.image = image

  def show(self):
    # plt.imshow(self.image)
    plt.imshow(self.preprocess(self.image))
    plt.show()

  def reward(self):
    return 0

  @staticmethod
  def preprocess(image):
    image = image[100:600,50:1000]
    image[image == BACKGROUND] = BLACK
    image[image == BOARDER] = BLACK
    image[image == BLUE_TILE] = WHITE
    image[image == WHITE_TILE] = WHITE
    image = imresize(image, 0.5)
    return image

  @classmethod
  def gen(klass, name, simulator):
    state = simulator.state
    image = klass.preprocess(simulator.capture())
    return klass(state, image)
