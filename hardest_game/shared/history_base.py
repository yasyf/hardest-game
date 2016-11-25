from __future__ import division
from collections import deque
import numpy as np

class HistoryBase(object):
  HISTORY_SIZE = None
  INPUT_DIMS = None

  def __init__(self):
    self.reset()

  def reset(self):
    self.samples = deque()
    self.data = None
    self.last_data = None

  def add(self, sample):
    if not len(self.samples):
      self.samples.extend([sample] * self.HISTORY_SIZE)
      self.data = self.last_data = self._stacked_images()
    else:
      self.samples.popleft()
      self.samples.append(sample)
      self.last_data, self.data = self.data, self._stacked_images()

  def get(self, i=1):
    return self.samples[-i]

  def _stacked_images(self):
    return np.stack([sample.image for sample in self.samples], axis=-1)
