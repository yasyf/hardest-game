from __future__ import print_function, division
from test_agent import TestAgent
import copy, random
import numpy as np

class GreedyTester(TestAgent):
  EPSILON = 0.05
  NAME = 'Greedy'

  def next_action(self):
    if np.random.random() < self.EPSILON:
      return random.choice(list(self.Simulator.Move))

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

