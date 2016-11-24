from enum import IntEnum, unique

@unique
class ToyGameMove(IntEnum):
  left = 0
  right = 1
  stay = 2
