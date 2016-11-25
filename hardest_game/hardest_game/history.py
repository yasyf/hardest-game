from ..shared.history_base import HistoryBase
from .sample import HardestGameSample as Sample

class HardestGameHistory(HistoryBase):
  HISTORY_SIZE = 4
  INPUT_DIMS = Sample.IMAGE_DIMS + (HISTORY_SIZE,)
