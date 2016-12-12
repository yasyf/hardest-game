from __future__ import print_function, division
from ..shared.agent import Agent
from test_agent_mixin import TestAgentMixin
import random
import numpy as np

RUNS = 1000

class RandomTester(Agent, TestAgentMixin):
  def next_action(self):
    return random.choice(list(self.Simulator.Move))

  def _step(self):
    action, memory = self._make_next_move()
    if memory.is_terminal:
      return memory

  def test(self):
    runs = np.zeros(RUNS)

    for i in range(RUNS):
      self.reset()
      while True:
        memory = self._step()
        if memory:
          break
      runs[i] = memory.is_win

    print('Random Wins: {}%'.format(np.mean(runs) * 100))
