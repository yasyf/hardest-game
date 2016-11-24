from abc import abstractmethod
import matplotlib.pyplot as plt
from pickleable import Pickleable

class SampleBase(Pickleable):
  IMAGE_DIMS = None

  def __init__(self, state, image):
    self.state = state
    self.image = self.preprocess(image)

  def show(self):
    plt.imshow(self.image, cmap=plt.get_cmap('gray'))
    plt.show()

  @abstractmethod
  def preprocess(self, image):
    raise NotImplementedError

  @classmethod
  def gen(klass, name, simulator):
    return klass(simulator.state, simulator.capture())
