class Area(object):
  def __init__(self, x, y, width, height):
    self.x = x
    self.y = y
    self.width = width
    self.height = height

  @classmethod
  def from_target(klass, simulator, target):
    return klass(
      simulator.get_property(target, 'x'),
      simulator.get_property(target, 'y'),
      simulator.get_property(target, 'width'),
      simulator.get_property(target, 'height'),
    )
