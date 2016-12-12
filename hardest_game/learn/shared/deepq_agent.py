from agent import Agent
from ..net.deepq import DeepQ
import tensorflow as tf

class DeepQAgent(Agent):
  CONV_TEMPLATES = [('c1', 16, 8, 4), ('c2', 32, 4, 2)] # [(name, nout, size, stride)]
  FC_TEMPLATES = [('f1', 256)] # [(name, nout)]
  NOIMAGE_FC_TEMPLATES = [('f1', 128), ('f2', 64)] # [(name, nout)]

  def __init__(self, Simulator, verbose=False, restore=False, log=True):
    super(DeepQAgent, self).__init__(Simulator, verbose=verbose)
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
