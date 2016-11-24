import copy
import hashlib

class StateBase(object):
  def __init__(self, moves):
    self.moves = moves

  @staticmethod
  def id_for_moves(moves):
    return hashlib.md5(''.join(map(lambda x: str(x.value), moves))).hexdigest()

  def id(self):
    return self.id_for_moves(self.moves)

  def copy(self):
    return copy.deepcopy(self)
