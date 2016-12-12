from abc import abstractmethod

class ReplayMemoryBase(object):
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

  @abstractmethod
  def _calc_reward(self):
    raise NotImplementedError

  @abstractmethod
  def _calc_is_terminal(self):
    raise NotImplementedError

  @property
  def is_win(self):
    return self.next_state.is_win()

  @property
  def is_death(self):
    return self.next_state.is_death()
