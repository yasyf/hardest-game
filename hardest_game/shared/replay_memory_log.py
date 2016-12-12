from __future__ import division
from collections import deque
import random

REPLAY_MEMORY_SIZE = 1e5

class ReplayMemoryLog(object):
  MINIBATCH_SIZE = 32

  def __init__(self, ReplayMemory, history):
    self.memories = deque()
    self.history = history
    self.ReplayMemory = ReplayMemory

  def snapshot(self):
    memory = self.ReplayMemory(self.history)
    if len(self.memories) >= REPLAY_MEMORY_SIZE:
      self.memories.popleft()
    self.memories.append(memory)
    return memory

  def sample_minibatch(self):
    return random.sample(self.memories, min(len(self.memories), self.MINIBATCH_SIZE))
