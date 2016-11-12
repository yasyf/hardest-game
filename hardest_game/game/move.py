from enum import IntEnum, unique

@unique
class Move(IntEnum):
  up = 0
  down = 1
  left = 2
  right = 3
  stay = 4
