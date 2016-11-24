from move import Move

ENDGAME_REWARD = 1000
COIN_REWARD = 10
MOVEMENT_REWARD = 0.01

class ReplayMemory(object):
  def __init__(self, history):
    self.state = history.get(2).state
    self.next_state = history.get().state

    self.data = history.last_data
    self.next_data = history.data

    self.reward = self._calc_reward()
    self.is_terminal = self._calc_is_terminal()

  @property
  def action(self):
    return self.next_state.moves[-1]

  def _calc_reward(self):
    if self.next_state.is_death():
      return -ENDGAME_REWARD
    if self.next_state.is_win():
      return ENDGAME_REWARD

    if self.state.level.start.contains(self) and not self.did_move():
      return -COIN_REWARD

    return (
      (COIN_REWARD * self.coins_gained())
      + self.log_distance_reduced()
      + (MOVEMENT_REWARD * (1 if self.did_move() else -1))
    )

  def _calc_is_terminal(self):
    return self.next_state.is_death() or self.next_state.is_win()

  def log_distance_reduced(self):
    return (self.state.log_distance_to_end() - self.next_state.log_distance_to_end()) / 10.

  def coins_gained(self):
    return self.next_state.coins - self.state.coins

  def did_move(self):
    return self.action != Move.stay
