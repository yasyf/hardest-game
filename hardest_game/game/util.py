import os

def static_dir(*path):
  return os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'static', *path))

data_file = lambda *path: static_dir('data', *path)

def to_enum(val, klass):
  if isinstance(val, klass):
    return klass
  try:
    return klass(val)
  except ValueError:
    return klass[val]
