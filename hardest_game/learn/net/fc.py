import tensorflow as tf
from .base import Base

class FC(Base):
  def __init__(
    self,
    name,
    input_tensor,
    noutput,
    activation_fn=tf.nn.relu,
  ):
    self.name = name
    self.input = input_tensor
    self.noutput = noutput
    self.activation_fn = activation_fn

    with tf.variable_scope('fc'):
      self.out = tf.contrib.layers.fully_connected(
        input_tensor,
        noutput,
        activation_fn,
        name=name
      )

  def to_tf(self):
    return self.out
