import tensorflow as tf
from .base import Base

class Conv2D(Base):
  def __init__(
    self,
    name,
    input_tensor,
    noutput,
    filter_dims,
    stride,
    padding='SAME',
    activation_fn=tf.nn.relu,
  ):
    self.name = name
    self.input = input_tensor
    self.noutput = noutput
    self.filter_dims = filter_dims
    self.stride = stride
    self.padding = padding
    self.activation_fn = activation_fn

    with tf.variable_scope('conv2d'):
      self.out = tf.contrib.layers.convolution2d(
        input_tensor,
        noutput,
        filter_dims,
        activation_fn,
        [stride, stride],
        padding=padding,
        name=name
      )

  def to_tf(self):
    return self.out
