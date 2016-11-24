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

    level = level or Level.default()
    self._state = State(0, True, level, [])
    self.level = level
    self.frame = 0

  def _start(self):
    pass

  def _quit(self):
    pass

  @property
  def state(self):
    return self._state.copy()

  @property
  def enemy_present(self):
    return self.frame % self.level.enemy_phase == 0

  def _check_collision(self):
    if not self._state.alive:
      return True
    if self.enemy_present and self._state.x == self.level.enemy_loc:
      self._state.alive = False
      return True
    return False

  def _make_move(self, move):
    self.frame += 1

    if move == Move.left:
      self._state.x -= 1
    elif move == Move.right:
      self._state.x += 1
    elif move == Move.stay:
      pass
    else:
      raise ValueError(move)

    return self._check_collision()

  def capture(self):
    return self._state.draw(self.frame)
