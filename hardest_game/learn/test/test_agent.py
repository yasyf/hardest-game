from ..shared.agent import Agent
import matplotlib.pyplot as plt
import time
import numpy as np
from tqdm import trange

RUNS = 1000
NUM_STEPS = int(1e3)

class TestAgent(Agent):
  def _show(self):
    plt.ion()
    time.sleep(0.5)
    self.simulator.capture().show()
    time.sleep(0.5)

  def _step(self):
    action, memory = self._make_next_move()
    if memory.is_terminal:
      return memory

  def test(self, j):
    runs = np.zeros(RUNS, dtype=np.bool)

    for i in trange(RUNS):
      self.reset()
      for _ in xrange(NUM_STEPS):
        memory = self._step()
        if memory:
          runs[i] = memory.is_win
          break

    win_rate = np.mean(runs)
    print('{}[{}] Wins: {}%'.format(self.NAME, j, win_rate * 100))

    return win_rate

  def run_tests(self, n):
    win_rate = np.mean([self.test(i) for i in xrange(n)])
    print('{} Total Wins: {}%'.format(self.NAME, win_rate * 100))
