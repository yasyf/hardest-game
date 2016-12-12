from ..toy_game.simulator import ToyGameSimulator
from level import Level
from move import ToyGame2DMove as Move
from history import ToyGame2DHistory as History
from replay_memory import ToyGame2DReplayMemory as ReplayMemory
from sample import ToyGame2DSample as Sample
from state import ToyGame2DState as State

class ToyGame2DSimulator(ToyGameSimulator):
  Move = Move
  History = History
  ReplayMemory = ReplayMemory
  Sample = Sample
  State = State

  def _start(self):
    super(ToyGame2DSimulator, self)._start()
    self.level = self._level or Level.default()
    self._y = 0

  @property
  def y(self):
    return self._y

  @y.setter
  def y(self, new_y):
    new_y = int(new_y)
    if new_y < 0:
      self._y = 0
    elif new_y > State.MAX_Y:
      self._y = State.MAX_Y
    else:
      self._y = new_y

  @property
  def state(self):
    return self.__class__.State(self.x, self.y, self.frame, self.alive, self.level, self.moves)

  def _check_collision(self):
    if not self.alive:
      return True
    if self.state.enemy_shown() and (self.x, self.y) == self.level.enemy_loc:
      self.alive = False
      return True
    return False

  def _make_move(self, move):
    self.frame += 1

    if move == Move.left:
      self.x -= 1
    elif move == Move.right:
      self.x += 1
    elif move == Move.up:
      self.y -= 1
    elif move == Move.down:
      self.y += 1
    elif move == Move.stay:
      pass
    else:
      raise ValueError(move)

    return self._check_collision()
