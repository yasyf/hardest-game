from .base import Base
from .conv2d import Conv2D
from .fc import FC
import tensorflow as tf

class DeepQ(Base):
  def __init__(self, input_dims, conv_templates, fc_templates, nactions):
    self.input_dims = input_dims
    self.conv_templates = conv_templates
    self.fc_templates = fc_templates
    self.nactions = nactions

    (height, width, ninput) = input_dims
    with tf.variable_scope('deepq'):
      self.input = tf.placeholder(tf.float32, [None, height, width, ninput], 'input')
      self._create_conv_layers()
      self._create_fc_layers()
      self.out = FC('output', self.fc_layers[-1], nactions, activation_fn=None).to_tf()

  def _create_conv_layers(self):
    self.conv_layers = []
    input_ = self.input
    for (name, n, size, stride) in self.conv_templates:
      out = Conv2D(name, input_, n, [size, size], stride).to_tf()
      self.conv_layers.append(out)
      input_ = out

  def _create_fc_layers(self):
    self.fc_layers = []
    input_ = self.conv_layers[-1]
    for (name, n) in self.fc_templates:
      out = FC(name, input_, n).to_tf()
      self.fc_layers.append(out)
      input_ = out

  def to_tf(self):
    return self.out
