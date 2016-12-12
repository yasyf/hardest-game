from ..shared.replay_memory_base import ReplayMemoryBase
from move import HardestGameMove as Move

ENDGAME_REWARD = 1000
COIN_REWARD = 10
MOVEMENT_REWARD = 0.1

class HardestGameReplayMemory(ReplayMemoryBase):
  def _calc_reward(self):
    if self.is_death:
      return -ENDGAME_REWARD
    if self.is_win:
      return ENDGAME_REWARD

    did_move = self.did_move()

    if self.state.is_start():
      if did_move:
        return 0
      else:
        return -1

    return (
      (COIN_REWARD * self.coins_gained())
      + self.log_distance_reduced()
      + (MOVEMENT_REWARD * (1 if did_move else -1))
    )

  def _calc_is_terminal(self):
    return self.is_death or self.is_win

  def log_distance_reduced(self):
    return (self.state.log_distance_to_end() - self.next_state.log_distance_to_end()) / 10.

  def coins_gained(self):
    return self.next_state.coins - self.state.coins

  def did_move(self):
    return self.action != Move.stay and (self.next_state.x != self.state.x or self.next_state.y != self.state.y)
