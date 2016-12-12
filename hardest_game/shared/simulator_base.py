import logging
from abc import abstractmethod, abstractproperty
from util import to_enum

class GameError(Exception):
  pass

class GameEndError(GameError):
  pass

class SimulatorBase(object):
  Move = None
  ReplayMemory = None
  Sample = None
  State = None

  def __init__(self, name='Simulator', verbose=True, moves=None):
    self.name = name
    self.verbose = verbose
    self.moves = moves or []

  def log(self, *args):
    message = '[{}]: {}'.format(self.name, ' '.join(map(str, args)))
    if self.verbose:
      logging.warning(message)
    else:
      logging.info(message)

  @abstractmethod
  def _start(self):
    raise NotImplementedError

  def start(self):
    self._start()
    moves, self.moves = self.moves, []
    self.make_moves(moves)

  def restart(self):
    self.moves = []
    self._quit()
    self._start()

  @abstractmethod
  def _quit(self):
    raise NotImplementedError

  def quit(self):
    try:
      self._quit()
    except:
      pass

  def __enter__(self):
    self.start()
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    self.quit()

  def __del__(self):
    self.quit()

  @abstractproperty
  def state(self):
    raise NotImplementedError

  @abstractproperty
  def _make_move(self, move):
    raise NotImplementedError

  def make_move(self, move, raise_on_death=False):
    move = to_enum(move, self.__class__.Move)
    end = self._make_move(move)
    self.moves.append(move)
    if end and raise_on_death:
      raise GameEndError('death!')

  def make_moves(self, moves):
    for move in moves:
      self.make_move(move)

  @abstractmethod
  def capture(self):
    raise NotImplementedError

  def sample(self, use_cached=False):
    if use_cached:
      return self.__class__.Sample.load_or_gen(self.state.id(), self)
    else:
      return self.__class__.Sample.gen(None, self)
