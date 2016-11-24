from ..shared.replay_memory_base import ReplayMemoryBase

REWARD = 1

class ToyGameReplayMemory(ReplayMemoryBase):
  def _calc_reward(self):
    if not self.next_state.alive:
      return -REWARD

    if self.next_state.is_win():
      return REWARD

    return 0

  def _calc_is_terminal(self):
    return (not self.next_state.alive) or self.next_state.is_win()
