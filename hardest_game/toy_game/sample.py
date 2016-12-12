import numpy as np
from .state import ToyGameState
from ..shared.sample_base import SampleBase
from ..shared.util import GREYSCALE

class ToyGameSample(SampleBase):
  USE_IMAGE = False
  IMAGE_DIMS = (20, 80) if USE_IMAGE else (ToyGameState.MAX_X + 1,)

  if USE_IMAGE:
    def preprocess(self, image):
      image = np.dot(image, GREYSCALE)
      return image
  else:
    def preprocess(self, image):
      return image

    @classmethod
    def gen(klass, name, simulator):
      return klass(simulator.state, simulator.state.feature_vector())
