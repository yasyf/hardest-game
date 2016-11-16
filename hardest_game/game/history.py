from __future__ import division
from collections import deque
import numpy as np

class History(object):
  HISTORY_SIZE = 4

  def __init__(self):
    self.reset()

  def reset(self):
    self.samples = deque()

  def add(self, sample):
    if not len(self.samples):
      self.samples.extend([sample] * self.HISTORY_SIZE)
    else:
      self.samples.popleft()
      self.samples.append(sample)

  def get(self, i=1):
    return self.samples[-i]

  def stacked_images(self):
    return np.stack([sample.image for sample in self.samples], axis=-1)
