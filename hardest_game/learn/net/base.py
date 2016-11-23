from abc import abstractmethod

class Base(object):
  @abstractmethod
  def to_tf(self):
    raise NotImplementedError
