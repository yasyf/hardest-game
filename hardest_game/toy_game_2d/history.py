from .sample import ToyGame2DSample as Sample
from ..toy_game.history import ToyGameHistory

class ToyGame2DHistory(ToyGameHistory):
  if Sample.USE_IMAGE:
    INPUT_DIMS = Sample.IMAGE_DIMS + (ToyGameHistory.HISTORY_SIZE,)
  else:
    INPUT_DIMS = (Sample.IMAGE_DIMS[0] * ToyGameHistory.HISTORY_SIZE,)
