import cPickle as pickle
from util import data_file
import os

klass_path = lambda klass: data_file(klass.__name__.lower())
klass_name_path = lambda klass, name: os.path.join(klass_path(klass), name + '.pickle')

class Pickleable(object):
  __cache = {}

  @classmethod
  def load_or_gen(klass, name, *args, **kwargs):
    try:
      return klass.load(name)
    except ValueError:
      value = klass.gen(name, *args, **kwargs)
      klass.save(name , value)
      return value

  @classmethod
  def load(klass, name):
    parent_path = klass_path(klass)
    path = klass_name_path(klass, name)
    if path in klass.__cache:
      return klass.__cache[path]
    if not os.path.exists(parent_path):
      os.makedirs(parent_path)
    if not os.path.exists(path):
      raise ValueError(path)
    with open(path, 'r') as f:
      value = pickle.load(f)
      klass.__cache[path] = value
      return value

  @classmethod
  def save(klass, name, value):
    path = klass_name_path(klass, name)
    klass.__cache[path] = value
    with open(path, 'w') as f:
      pickle.dump(value, f)
