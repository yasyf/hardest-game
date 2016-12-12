from ..shared.pickleable import Pickleable
from area import Area

class Level(Pickleable):
  def __init__(self, number, coins, start, end):
    self.number = number
    self.coins = coins
    self.start = start
    self.end = end

  @classmethod
  def gen(klass, name, simulator):
    level = int(name)
    coins = simulator.get_variable('coins').split(',')[level - 1]
    start = Area.from_target(simulator, 'check1')
    end = Area.from_target(simulator, 'check2')
    return klass(level, coins, start, end)
