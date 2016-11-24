import numpy as np
from ..shared.sample_base import SampleBase
from ..shared.util import GREYSCALE

class ToyGameSample(SampleBase):
  IMAGE_DIMS = (20, 80)

  def preprocess(self, image):
    image = np.dot(image, GREYSCALE)
    return image
