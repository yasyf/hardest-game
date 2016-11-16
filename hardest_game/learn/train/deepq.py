from __future__ import print_function
from ...game.move import Move
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

  def _train_episode(self):
    pass

  def train(self):
    for i in range(NUM_EPISODES):
      print('Episode {}'.format(i))
      self._train_episode()
