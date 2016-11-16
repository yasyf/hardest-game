from abc import abstractmethod

class NetBase(object):
  @abstractmethod
  def to_tf(self):
    raise NotImplementedError
