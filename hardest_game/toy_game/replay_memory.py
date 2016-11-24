from ..shared.replay_memory_base import ReplayMemoryBase
from move import ToyGameMove as Move

REWARD = 10
MOVEMENT_REWARD = 0.1

class ToyGameReplayMemory(ReplayMemoryBase):
  def _calc_reward(self):
    if not self.next_state.alive:
      return -REWARD

    if self.next_state.is_win():
      return REWARD

    if self.did_move():
      return MOVEMENT_REWARD
    else:
      return -MOVEMENT_REWARD

  def _calc_is_terminal(self):
    return (not self.next_state.alive) or self.next_state.is_win()

  def did_move(self):
    return self.action != Move.stay and (self.next_state.x != self.state.x)
