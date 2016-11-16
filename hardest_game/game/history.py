from __future__ import division
from collections import deque

HISTORY_SIZE = 4

class History():
  def __init__(self):
    self.samples = deque()

  def add(self, sample):
    if not len(self.samples):
      self.samples.extend([sample] * HISTORY_SIZE)
    else:
      self.samples.popleft()
      self.samples.append(sample)

  def get(self, i=1):
    return self.samples[-i]
