from ..shared.history_base import HistoryBase
from .sample import ToyGameSample as Sample
import numpy as np

class ToyGameHistory(HistoryBase):
  HISTORY_SIZE = 2

  if Sample.USE_IMAGE:
    INPUT_DIMS = Sample.IMAGE_DIMS + (HISTORY_SIZE,)
  else:
    INPUT_DIMS = (Sample.IMAGE_DIMS[0] * HISTORY_SIZE,)

    def _stacked_images(self):
      return np.concatenate([sample.image for sample in self.samples], axis=-1)
