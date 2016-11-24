from __future__ import print_function, division
from ..shared.deepq_agent import DeepQAgent
import operator
import numpy as np
import random

EPSILON_LIFE = 1e3
NUM_EPISODES = int(1e3)
NUM_STEPS = int(1e5)
SAVE_EVERY = 10
GAMMA = 0.99

class DeepQTrainer(DeepQAgent):
  def __init__(self, Simulator, verbose=False):
    super(DeepQTrainer, self).__init__(Simulator, verbose=verbose)
    self.frameno = 0

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
    self.reset()

    for _ in range(NUM_STEPS):
      try:
        self._step()
      except StopIteration:
        break

  def _step(self):
    self.step += 1
    self.frameno += 1

    action, memory = self._make_next_move()
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
