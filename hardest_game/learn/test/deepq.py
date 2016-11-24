from __future__ import print_function, division
from ..shared.deepq_agent import DeepQAgent
import matplotlib.pyplot as plt
import time

class DeepQTester(DeepQAgent):
  def __init__(self, Simulator, verbose=True):
    super(DeepQTester, self).__init__(Simulator, verbose=verbose, restore=True)

  def next_action(self):
    return self.net.eval_best_action(self.history.data)

  def _step(self):
    action, memory = self._make_next_move()
    if memory.is_terminal:
      raise StopIteration

  def _show(self):
    time.sleep(0.5)
    self.history.get().show(ion=True)
    time.sleep(0.5)

  def test(self):
    plt.ion()
    self.reset()

    self._show()
    while True:
      self._show()
      try:
        self._step()
      except StopIteration:
        break
    self._show()
