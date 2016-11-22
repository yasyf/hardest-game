from __future__ import print_function, division
from ...game.move import Move
from ...game.replay_memory_log import ReplayMemoryLog
from ...game.simulator import Simulator
from ...game.history import History
from ...game.sample import Sample
from ..net.deepq import DeepQ
import operator
import numpy as np
import random

CONV_TEMPLATES = [('c1', 16, 8, 4), ('c2', 32, 4, 2)] # [(name, nout, size, stride)]
FC_TEMPLATES = [('f1', 256)] # [(name, nout)]
EPSILON_LIFE = 1e2
INPUT_DIMS = Sample.IMAGE_DIMS + (History.HISTORY_SIZE,)
NUM_EPISODES = 1e3
NUM_STEPS = 1e3
GAMMA = 0.99

class DeepQTrainer(object):
  def __init__(self):
    self.net = DeepQ(INPUT_DIMS, CONV_TEMPLATES, FC_TEMPLATES, len(Move))
    self.saver = tf.train.Saver()
    self.frameno = 0
    self.simulator = Simulator()
    self.history = History()
    self.replay_memories = ReplayMemoryLog(self.history)

    self.simulator.start()

  @property
  def epsilon(self):
    if self.frameno > EPSILON_LIFE:
      return 0.1
    else:
      return 1. - (0.9 * (self.frameno / EPSILON_LIFE))

  def next_action(self):
    if np.random.random() < self.epsilon:
      return random.choice(list(Move))
    else:
      return self.net.best_action(self.history.data)

  def _label_for_memory(self, memory):
    if memory.is_terminal:
      return memory.reward
    else:
      return memory.reward + (GAMMA * self.net.best_reward(memory.next_data))

  def _train_episode(self):
    self.history.reset()
    for _ in range(History.HISTORY_SIZE):
      self.history.add(self.simulator.sample(use_cached=False))

    for _ in range(NUM_STEPS):
      try:
        self._step()
      except StopIteration:
        break

  def _step(self):
    action = self.next_action()
    self.simulator.make_move(action)
    self.history.add(self.simulator.sample())
    memory = self.replay_memories.snapshot()

    minibatch = self.replay_memories.sample_minibatch()
    data = np.array(map(operator.attrgetter('data'), minibatch))
    labels = np.array(map(self._label_for_memory, minibatch))
    self.net.train(data, labels)

    if memory.is_terminal:
      raise StopIteration

  def train(self):
    for i in range(NUM_EPISODES):
      print('Episode {}'.format(i))
      self._train_episode()
