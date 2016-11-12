from move import Move
from pickleable import Pickleable
from scipy.misc import imresize
import matplotlib.pyplot as plt
import numpy as np

ENDGAME_REWARD = 1000
COIN_REWARD = 50
MOVEMENT_REWARD = 10

BLACK = 0
WHITE = 255
BACKGROUND = [180, 181, 254]
BOARDER = [124, 124, 175]
BLUE_TILE = [230, 230, 255]
WHITE_TILE = [247, 247, 255]
GREYSCALE = [0.299, 0.587, 0.114]

class Sample(Pickleable):
  def __init__(self, state, image):
    self.state = state
    self.image = image

  def show(self):
    plt.imshow(self.image, cmap=plt.get_cmap('gray'))
    plt.show()

  def reward(self):
    if self.state.deaths > 0:
      return -ENDGAME_REWARD
    if self.state.level.coins == self.state.coins and self.state.level.end.contains(self.state):
      return ENDGAME_REWARD

    difference = (self.state.level.end.x - self.state.x, self.state.level.end.y - self.state.y)
    did_move = self.state.history[-1] != Move.stay
    return (COIN_REWARD * self.state.coins) - np.log(np.linalg.norm(difference)) + (MOVEMENT_REWARD * int(did_move))

  @staticmethod
  def preprocess(image):
    image = image[100:600,50:1000]
    image[image == BACKGROUND] = BLACK
    image[image == BOARDER] = BLACK
    image[image == BLUE_TILE] = WHITE
    image[image == WHITE_TILE] = WHITE
    image = np.dot(image, GREYSCALE)
    image = imresize(image, 0.5)
    return image

  @classmethod
  def gen(klass, name, simulator):
    state = simulator.state
    image = klass.preprocess(simulator.capture())
    return klass(state, image)
