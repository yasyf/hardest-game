from __future__ import division
from scipy.misc import imresize
import numpy as np
from ..shared.sample_base import SampleBase
from ..shared.util import GREYSCALE, BLACK, WHITE

IMSCALE = 1/2
BACKGROUND = [180, 181, 254]
BOARDER = [124, 124, 175]
BLUE_TILE = [230, 230, 255]
WHITE_TILE = [247, 247, 255]

class HardestGameSample(SampleBase):
  IMAGE_DIMS = (250, 475)

  def preprocess(self, image):
    image = image[100:600,50:1000]
    image[image == BACKGROUND] = BLACK
    image[image == BOARDER] = BLACK
    image[image == BLUE_TILE] = WHITE
    image[image == WHITE_TILE] = WHITE
    image = np.dot(image, GREYSCALE)
    image = imresize(image, IMSCALE, interp='bilinear')
    return image
