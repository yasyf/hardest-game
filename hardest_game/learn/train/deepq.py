from __future__ import print_function, division
from ...shared.history import History
from ...shared.replay_memory_log import ReplayMemoryLog
from ..net.deepq import DeepQ
import operator
import numpy as np
import tensorflow as tf
import random

CONV_TEMPLATES = [('c1', 16, 8, 4), ('c2', 32, 4, 2)] # [(name, nout, size, stride)]
FC_TEMPLATES = [('f1', 256)] # [(name, nout)]
EPSILON_LIFE = 1e3
NUM_EPISODES = int(1e3)
NUM_STEPS = int(1e5)
SAVE_EVERY = 10
GAMMA = 0.99

class DeepQTrainer(object):
  def __init__(self, Simulator, verbose=False):
    self.Simulator = Simulator
    self.session = tf.Session()
    self.net = DeepQ(
      Simulator.Sample.IMAGE_DIMS + (History.HISTORY_SIZE,),
      CONV_TEMPLATES,
      FC_TEMPLATES,
      len(Simulator.Move),
      self.session,
    )
    self.frameno = 0
    self.history = History()
    self.replay_memories = ReplayMemoryLog(Simulator.ReplayMemory, self.history)
    self.verbose = verbose

  def reset_simulator(self):
    if hasattr(self, 'simulator'):
      self.simulator.restart()
    else:
      self.simulator = self.Simulator(verbose=self.verbose)
      self.simulator.start()

  @property
  def epsilon(self):
    if self.frameno > EPSILON_LIFE:
      return 0.1
    else:
      return 1. - (0.9 * (self.frameno / EPSILON_LIFE))

  def next_action(self):
    if np.random.random() < self.epsilon:
      return random.choice(list(self.Simulator.Move))
    else:
      return self.net.eval_best_action(self.history.data)

  def _label_for_memory(self, memory):
    if memory.is_terminal:
      return memory.reward
    else:
      return memory.reward + (GAMMA * self.net.eval_best_reward(memory.next_data))

  def _train_episode(self):
    self.step = 0
    self.history.reset()
    self.reset_simulator()

    for _ in range(History.HISTORY_SIZE):
      self.history.add(self.simulator.sample())

    for _ in range(NUM_STEPS):
      try:
        self._step()
      except StopIteration:
        break

  def _step(self):
    self.step += 1
    self.frameno += 1

    action = self.next_action()
    self.simulator.make_move(action)
    self.history.add(self.simulator.sample())
    memory = self.replay_memories.snapshot()

    if self.verbose:
      print('Action: {}, Reward: {}'.format(action, memory.reward))

    minibatch = self.replay_memories.sample_minibatch()
    data = np.array(map(operator.attrgetter('data'), minibatch))
    actions = np.array(map(operator.attrgetter('action'), minibatch))
    labels = np.array(map(self._label_for_memory, minibatch))

    if self.verbose:
      loss = self.net.train_loss(data, actions, labels)
      print('Loss: {}'.format(loss))
    else:
      self.net.train(data, actions, labels)

    if memory.is_terminal:
      print('Final Reward: {}'.format(memory.reward))
      raise StopIteration

  def train(self):
    for i in range(NUM_EPISODES):
      print('Episode {}'.format(i))
      self._train_episode()
      if i % SAVE_EVERY == 0:
        self.net.save()
