from ..toy_game_2d.simulator import ToyGame2DSimulator
from level import Level
from move import ToyGame2DHardMove as Move
from history import ToyGame2DHardHistory as History
from replay_memory import ToyGame2DHardReplayMemory as ReplayMemory
from sample import ToyGame2DHardSample as Sample
from state import ToyGame2DHardState as State

class ToyGame2DHardSimulator(ToyGame2DSimulator):
  Move = Move
  History = History
  ReplayMemory = ReplayMemory
  Sample = Sample
  State = State

  def _start(self):
    super(ToyGame2DHardSimulator, self)._start()
    self.level = self._level or Level.default()

  def _check_collision(self):
    if not self.alive:
      return True
    if self.state.enemy_at_loc((self.x, self.y)):
      self.alive = False
      return True
    return False
