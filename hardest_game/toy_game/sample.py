import numpy as np
from .state import ToyGameState
from ..shared.sample_base import SampleBase
from ..shared.util import GREYSCALE

class ToyGameSample(SampleBase):
  USE_IMAGE = True
  IMAGE_DIMS = (20, 80) if USE_IMAGE else (ToyGameState.MAX_X,)

  def preprocess(self, image):
    if self.__class__.USE_IMAGE:
      image = np.dot(image, GREYSCALE)
      return image
    else:
      return self.state.feature_vector()
