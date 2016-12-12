from __future__ import print_function, division
from ..shared.deepq_agent import DeepQAgent
from test_agent_mixin import TestAgentMixin

class DeepQTester(DeepQAgent, TestAgentMixin):
  def __init__(self, Simulator, verbose=True):
    super(DeepQTester, self).__init__(Simulator, verbose=verbose, restore=True, log=False)

  def next_action(self):
    return self.net.eval_best_action(self.history.data)

  def _step(self):
    action, memory = self._make_next_move()
    if memory.is_terminal:
      raise StopIteration

  def test(self):
    self.reset()

    self._show()
    while True:
      self._show()
      try:
        self._step()
      except StopIteration:
        break
    self._show()
