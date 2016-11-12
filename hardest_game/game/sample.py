from pickleable import Pickleable

LARGE_NUMBER = 1000

class Sample(Pickleable):
  def __init__(self, state, image):
    self.state = state
    self.image = image

  @staticmethod
  def preprocess(image):
    return image

  @classmethod
  def gen(klass, name, simulator):
    state = simulator.state
    image = klass.preprocess(simulator.capture())
    return klass(state, image)
