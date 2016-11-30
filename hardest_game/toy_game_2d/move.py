from enum import IntEnum, unique

@unique
class ToyGame2DMove(IntEnum):
  left = 0
  right = 1
  up = 2
  down = 3
  stay = 4
