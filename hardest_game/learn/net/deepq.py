import time
from .base import Base
from .conv2d import Conv2D
from .fc import FC
import tensorflow as tf
from ...game.util import static_dir

DELTA_MIN = -10
DELTA_MAX = 10
LEARNING_RATE_MIN = 0.0000025
LEARNING_RATE_START = 0.000025
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

    (height, width, ninput) = input_dims
    with tf.variable_scope('deepq'):
      self.data = tf.placeholder(tf.float32, [None, height, width, ninput], 'data')
      self.actions = tf.placeholder(tf.int32, [None], 'actions')
      self.labels = tf.placeholder(tf.float32, [None], 'labels')
      self._create_conv_layers()
      self._create_fc_layers()
      self._add_out()
      self._add_loss()
      self._add_optimizer()
      self._add_summaries()

    if restore:
      self.saver.restore(self.session, MODEL_DIR)
    else:
      init = tf.initialize_all_variables()
      self.session.run(init)

    self.saver = tf.train.Saver()
    log_dir = static_dir('tf', 'logs', str(int(time.time())))
    self.writer = tf.train.SummaryWriter(log_dir, self.session.graph)

  def _create_conv_layers(self):
    self.conv_layers = []
    input_ = self.data
    for (name, n, size, stride) in self.conv_templates:
      out = Conv2D(name, input_, n, [size, size], stride).to_tf()
      self.conv_layers.append(out)
      input_ = out

  def _create_fc_layers(self):
    self.fc_layers = []
    input_ = tf.contrib.layers.flatten(self.conv_layers[-1])
    for (name, n) in self.fc_templates:
      out = FC(name, input_, n).to_tf()
      self.fc_layers.append(out)
      input_ = out

  def _add_out(self):
    self.out = FC('output', self.fc_layers[-1], self.nactions, activation_fn=None).to_tf()
    self.best_action = tf.argmax(self.out, dimension=1)
    self.best_reward = tf.reduce_max(self.out, reduction_indices=1)

  def _add_loss(self):
    actions_one_hot = tf.one_hot(self.actions, self.nactions, name='actions_one_hot')
    q_estimate = tf.reduce_sum(self.out * actions_one_hot, reduction_indices=1, name='q_estimate')
    delta = tf.clip_by_value(self.labels - q_estimate, DELTA_MIN, DELTA_MAX, name='delta')
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
    for i in range(self.nactions):
      tf.histogram_summary('q[{}]'.format(i), averaged_out[i])

    self.summaries = tf.merge_all_summaries()

  def save(self):
    self.saver.save(self.session, MODEL_DIR, global_step=self.global_step)

  def train(self, data, actions, labels):
    _, loss, summary = self.session.run([self.optimizer, self.loss, self.summaries], {
      self.data: data,
      self.actions: actions,
      self.labels: labels,
    })
    self.writer.add_summary(summary, global_step=tf.train.global_step(self.session, self.global_step))
    return loss

  def eval_best_action(self, data):
    return self.best_action.eval({self.data: [data]}, session=self.session)[0]

  def eval_best_reward(self, data):
    return self.best_reward.eval({self.data: [data]}, session=self.session)[0]

  def to_tf(self):
    return self.out
