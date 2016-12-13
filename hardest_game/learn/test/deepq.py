from __future__ import print_function, division
from ..shared.deepq_agent import DeepQAgent
from test_agent import TestAgent

class DeepQTester(DeepQAgent, TestAgent):
  NAME = 'DeepQ'

  def __init__(self, Simulator, verbose=False):
    super(DeepQTester, self).__init__(Simulator, verbose=verbose, restore=True, log=False)

  def next_action(self):
    return self.net.eval_best_action(self.history.data)
