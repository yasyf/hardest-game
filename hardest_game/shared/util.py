import os, functools, time

WAIT_DELAY = 0.05
WAIT_TIME = 0.5

GREYSCALE = [0.299, 0.587, 0.114]
BLACK = 0
WHITE = 255

def static_dir(*path):
  return os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'static', *path))

def ensure_exists(path):
  if not os.path.exists(os.path.dirname(path)):
    os.makedirs(os.path.dirname(path))
  return path

data_file = lambda *path: static_dir('data', *path)

def to_enum(val, klass):
  if isinstance(val, klass):
    return val
  try:
    return klass(val)
  except ValueError:
    return klass[val]

def waitable(f):
  @functools.wraps(f)
  def wrapped(*args, **kwargs):
    wait = kwargs.get('wait', True)
    val = f(*args, **kwargs)
    if not wait:
      return val
    for _ in range(int(WAIT_TIME / WAIT_DELAY)):
      if val is not None:
        return val
      time.sleep(WAIT_DELAY)
      val = f(*args, **kwargs)

    assert val is not None
    return val

  return wrapped
