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

    with tf.variable_scope(name):
      self.out = tf.contrib.layers.convolution2d(
        inputs=input_tensor,
        num_outputs=noutput,
        kernel_size=filter_dims,
        activation_fn=activation_fn,
        stride=[stride, stride],
        padding=padding,
        scope='conv2d',
      )

  def to_tf(self):
    return self.out
