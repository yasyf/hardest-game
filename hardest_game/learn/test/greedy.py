from __future__ import print_function, division
from ..shared.agent import Agent
from test_agent_mixin import TestAgentMixin
import copy
import numpy as np

RUNS = 1000

class GreedyTester(Agent, TestAgentMixin):
  def next_action(self):
    moves = {}
    for move in self.Simulator.Move:
      simulator = self.Simulator(verbose=False, moves=self.simulator.moves[:-1], level=self.simulator.level)
      simulator.start()
      simulator.make_move(move, raise_on_death=False)

      history = copy.deepcopy(self.history)
      history.add(simulator.sample())
      memory = self.Simulator.ReplayMemory(history)
      moves[move] = memory.reward

    return max(moves, key=moves.__getitem__)

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

    print('Greedy Wins: {}%'.format(np.mean(runs) * 100))

