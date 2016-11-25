import numpy as np
from .state import ToyGameState
from ..shared.sample_base import SampleBase
from ..shared.util import GREYSCALE

class ToyGameSample(SampleBase):
  USE_IMAGE = False
  IMAGE_DIMS = (20, 80) if USE_IMAGE else (ToyGameState.MAX_X + 1,)

  def preprocess(self, image):
    image = np.dot(image, GREYSCALE)
    return image

  @property
  def image(self):
    if self.__class__.USE_IMAGE:
      return self._image
    else:
      return self.state.feature_vector()
