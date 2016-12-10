from ..toy_game.sample import ToyGameSample
from .state import ToyGame2DState

class ToyGame2DSample(ToyGameSample):
  if not ToyGameSample.USE_IMAGE:
    IMAGE_DIMS = ((ToyGame2DState.MAX_X + 1) * (ToyGame2DState.MAX_Y + 1),)
