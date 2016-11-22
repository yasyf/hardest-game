from .base import Base
from .conv2d import Conv2D
from .fc import FC
import tensorflow as tf
import numpy as np
from ...game.util import static_dir

LEARNING_RATE_MIN = 0.00025
LEARNING_RATE_START = 0.1
LEARNING_RATE_DECAY = 0.96
LEARNING_RATE_STEP = 5 * 1e3
MOMENTUM = 0.95
MODEL_DIR = static_dir('tf', 'models')

class DeepQ(Base):
  def __init__(self, input_dims, conv_templates, fc_templates, nactions, session, restore=False):
    self.input_dims = input_dims
    self.conv_templates = conv_templates
    self.fc_templates = fc_templates
    self.nactions = nactions
    self.session = session
    self.saver = tf.train.Saver()

    (height, width, ninput) = input_dims
    with tf.variable_scope('deepq'):
      self.data = tf.placeholder(tf.float32, [None, height, width, ninput], 'data')
      self.actions = tf.placeholder(tf.int32, [None], 'actions')
      self.labels = tf.placeholder(tf.float32, [None], 'labels')
      self._create_conv_layers()
      self._create_fc_layers()
      self.out = FC('output', self.fc_layers[-1], nactions, activation_fn=None).to_tf()
      self._add_loss()
      self._add_optimizer()
      self._add_summaries()

    if restore:
      self.saver.restore(self.session, MODEL_DIR)
    else:
      init = tf.initialize_all_variables()
      self.session.run(init)

  def _create_conv_layers(self):
    self.conv_layers = []
    input_ = self.data
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

  def _add_loss(self):
    actions_one_hot = tf.one_hot(self.actions, self.nactions, name='actions_one_hot')
    q_estimate = tf.reduce_sum(self.out * actions_one_hot, reduction_indices=1, name='q_estimate')
    delta = self.labels - q_estimate
    self.loss = tf.reduce_mean(tf.square(delta), name='loss')

  def _add_optimizer(self):
    self.global_step = tf.Variable(0, name='global_step', trainable=False)
    self.learning_rate = tf.train.exponential_decay(
      LEARNING_RATE_START,
      self.global_step,
      LEARNING_RATE_STEP,
      LEARNING_RATE_DECAY,
    )
    learning_rate_op = tf.maximum(LEARNING_RATE_MIN, self.learning_rate)
    self.optimizer = tf.train.RMSPropOptimizer(learning_rate_op, momentum=MOMENTUM) \
                             .minimize(self.loss, global_step=self.global_step)

  def _add_summaries(self):
    tf.scalar_summary('learning_rate', self.learning_rate)

    averaged_out = tf.reduce_mean(self.out, reduction_indices=0)
    out_summaries = [tf.histogram_summary('q[{}]'.format(i), averaged_out[i]) for i in range(self.nactions)]
    self.out_summary = tf.merge_summary(out_summaries, 'out_summaries')

  def evaluate(self, data, actions):
    raise NotImplementedError

  def save(self):
    self.saver.save(self.session, MODEL_DIR, global_step=self.global_step)

  def train(self, data, actions, labels):
    self.session.run([self.optimizer, self.out, self.loss, self.out_summary], {
      self.data: data,
      self.actions: actions,
      self.labels: labels,
    })

  def best_action(self, phi):
    return np.argmax(self.evaluate(phi))

  def best_reward(self, phi):
    return np.max(self.evaluate(phi))

  def to_tf(self):
    return self.out
