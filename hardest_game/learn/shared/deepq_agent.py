from ...shared.replay_memory_log import ReplayMemoryLog
from ..net.deepq import DeepQ
from abc import abstractmethod
import tensorflow as tf

class DeepQAgent(object):
  CONV_TEMPLATES = [('c1', 16, 8, 4), ('c2', 32, 4, 2)] # [(name, nout, size, stride)]
  FC_TEMPLATES = [('f1', 256)] # [(name, nout)]
  NOIMAGE_FC_TEMPLATES = [('f1', 256), ('f2', 256)] # [(name, nout)]

  def __init__(self, Simulator, verbose=False, restore=False, log=True):
    self.Simulator = Simulator
    self.session = tf.Session()
    self.net = DeepQ(
      Simulator.__name__,
      Simulator.History.INPUT_DIMS,
      self.CONV_TEMPLATES if len(Simulator.Sample.IMAGE_DIMS) > 1 else [],
      self.FC_TEMPLATES if len(Simulator.Sample.IMAGE_DIMS) > 1 else self.NOIMAGE_FC_TEMPLATES,
      len(Simulator.Move),
      self.session,
      restore=restore,
      log=log,
    )
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
