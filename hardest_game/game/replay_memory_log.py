from __future__ import division
from .replay_memory import ReplayMemory
from collections import deque
import random

REPLAY_MEMORY_SIZE = 1e3

class ReplayMemoryLog(object):
  MINIBATCH_SIZE = 32

  def __init__(self, history):
    self.memories = deque()
    self.history = history

  def snapshot(self):
    memory = ReplayMemory(self.history)
    if len(self.memories) >= REPLAY_MEMORY_SIZE:
      self.memories.popleft()
    self.memories.append(memory)
    return memory

  def sample_minibatch(self):
    return random.sample(self.memories, self.MINIBATCH_SIZE)
