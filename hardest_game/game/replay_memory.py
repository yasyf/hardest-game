from move import Move

ENDGAME_REWARD = 1000
COIN_REWARD = 50
MOVEMENT_REWARD = 10

class ReplayMemory(object):
  def __init__(self, state, next_state):
    self.state = state
    self.next_state = next_state

  @property
  def action(self):
    return self.next_state.history[-1]

  @property
  def reward(self):
    if self.next_state.is_death():
      return -ENDGAME_REWARD
    if self.next_state.is_win():
      return ENDGAME_REWARD

    return (
      (COIN_REWARD * self.coins_gained())
      + self.log_distance_reduced()
      + (MOVEMENT_REWARD * int(self.did_move()))
    )

  def log_distance_reduced(self):
    return self.state.log_distance_to_end() - self.next_state.log_distance_to_end()

  def coins_gained(self):
    return self.next_state.coins - self.state.coins

  def did_move(self):
    return self.action != Move.stay
