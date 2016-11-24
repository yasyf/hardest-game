from ..shared.simulator_base import SimulatorBase
from level import Level
from move import ToyGameMove as Move
from replay_memory import ToyGameReplayMemory as ReplayMemory
from sample import ToyGameSample as Sample
from state import ToyGameState as State

class ToyGameSimulator(SimulatorBase):
  Move = Move
  ReplayMemory = ReplayMemory
  Sample = Sample
  State = State

  def __init__(self, level=None, *args, **kwargs):
    kwargs['name'] = kwargs.get('name', self.__class__.__name__)
    super(ToyGameSimulator, self).__init__(*args, **kwargs)
    self.level = level or Level.default()

  def _start(self):
    self.alive = True
    self._x = 0
    self.frame = 0

  def _quit(self):
    pass

  @property
  def x(self):
    return self._x

  @x.setter
  def x(self, new_x):
    new_x = int(new_x)
    if new_x < 0:
      self._x = 0
    elif new_x > State.MAX_X:
      self._x = State.MAX_X
    else:
      self._x = new_x

  @property
  def state(self):
    return State(self.x, self.alive, self.level, self.moves)

  @property
  def enemy_present(self):
    return self.frame % self.level.enemy_phase == 0

  def _check_collision(self):
    if not self.alive:
      return True
    if self.enemy_present and self.x == self.level.enemy_loc:
      self.alive = False
      return True
    return False

  def _make_move(self, move):
    self.frame += 1

    if move == Move.left:
      self.x -= 1
    elif move == Move.right:
      self.x += 1
    elif move == Move.stay:
      pass
    else:
      raise ValueError(move)

    return self._check_collision()

  def capture(self):
    return self.state.draw(self.frame)
