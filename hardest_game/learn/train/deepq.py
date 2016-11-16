from __future__ import print_function
from ...game.move import Move
from ...game.history import Simulator
from ...game.history import History
from ..net.deepq import DeepQ

CONV_TEMPLATES = [('c1', 16, 8, 4), ('c2', 32, 4, 2)] # [(name, nout, size, stride)]
FC_TEMPLATES = [('f1', 256)] # [(name, nout)]
REPLAY_MEMORY_SIZE = 1e9
INPUT_DIMS = (250, 475, HISTORY_SIZE)
NUM_EPISODES = 1e3

class DeepQTrainer(object):
  def __init__(self):
    self.net = DeepQ(INPUT_DIMS, CONV_TEMPLATES, FC_TEMPLATES, len(Move))
    self.replay_memories = []
    self.simulator = Simulator()

    self.simulator.start()

  def _train_episode(self):
    history = History()
    for _ in range(History.HISTORY_SIZE):
      history.add()

  def train(self):
    for i in range(NUM_EPISODES):
      print('Episode {}'.format(i))
      self._train_episode()
