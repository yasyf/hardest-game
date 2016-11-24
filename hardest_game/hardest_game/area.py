from __future__ import division

class Area(object):
  def __init__(self, x, y, width, height):
    self.x = float(x)
    self.y = float(y)
    self.width = int(width)
    self.height = int(height)

  def contains(self, other):
    return (self.x - (self.width / 2) <= other.x <= self.x + (self.width / 2)) and \
      (self.y - (self.height / 2) <= other.y <= self.y + (self.height / 2))

  @classmethod
  def from_target(klass, simulator, target):
    return klass(
      simulator.get_property(target, 'x'),
      simulator.get_property(target, 'y'),
      simulator.get_property(target, 'width'),
      simulator.get_property(target, 'height'),
    )
