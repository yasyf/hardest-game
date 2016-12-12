from ...shared.replay_memory_log import ReplayMemoryLog
from abc import abstractmethod

class Agent(object):
  def __init__(self, Simulator, verbose=False):
    self.Simulator = Simulator
    self.verbose = verbose
    self.history = Simulator.History()
    self.replay_memories = ReplayMemoryLog(Simulator.ReplayMemory, self.history)

  def reset_simulator(self):
    if hasattr(self, 'simulator'):
      self.simulator.restart()
    else:
      self.simulator = self.Simulator(verbose=self.verbose)
      self.simulator.start()

  def reset(self):
    self.reset_simulator()

    self.history.reset()
    for _ in range(self.Simulator.History.HISTORY_SIZE):
      self.simulator.make_move(self.Simulator.Move['stay'], raise_on_death=True)
      self.history.add(self.simulator.sample(use_cached=False))

  @abstractmethod
  def next_action(self):
    raise NotImplementedError

  def _make_next_move(self):
    action = self.next_action()
    self.simulator.make_move(action, raise_on_death=False)
    self.history.add(self.simulator.sample())
    memory = self.replay_memories.snapshot()

    if self.verbose:
      print('Action: {}, Reward: {}'.format(action, memory.reward))

    return action, memory
