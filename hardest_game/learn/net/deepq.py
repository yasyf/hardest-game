import time
from .base import Base
from .conv2d import Conv2D
from .fc import FC
import tensorflow as tf
from ...shared.util import static_dir, ensure_exists
import os

DELTA = 1
WRITE_SUMMARY_EVERY = 100

class DeepQ(Base):
  def __init__(self, name, input_dims, conv_templates, fc_templates, nactions, session, restore=False, log=True):
    model_dir = static_dir('tf', 'models', name)

    self.input_dims = input_dims
    self.conv_templates = conv_templates
    self.fc_templates = fc_templates
    self.nactions = nactions
    self.session = session
    self.model_file = ensure_exists(os.path.join(model_dir, 'deepq'))

    self._create_graph()

    self.log = log
    if log:
      log_dir = static_dir('tf', 'logs', str(int(time.time())))
      self.writer = tf.train.SummaryWriter(log_dir, self.session.graph)

    self._restore_or_init_vars(model_dir, restore)

  def _restore_or_init_vars(self, model_dir, restore):
    exists = os.path.exists(model_dir)
    if exists:
      checkpoint = tf.train.latest_checkpoint(model_dir)
    if restore and exists and checkpoint:
      self.saver.restore(self.session, checkpoint)
    else:
      init = tf.initialize_all_variables()
      self.session.run(init)

  def _create_graph(self):
    self.layers = []

    with tf.variable_scope('deepq'):
      self._create_input()
      self._create_conv_layers()
      self._create_fc_layers()
      self._add_out()
      self._add_loss()
      self._add_optimizer()
      self._add_summaries()
      self.saver = tf.train.Saver(max_to_keep=25, keep_checkpoint_every_n_hours=1)

  def _create_input(self):
    with tf.variable_scope('input'):
      self.data = tf.placeholder(tf.float32, [None] + list(self.input_dims), 'data')
      self.actions = tf.placeholder(tf.int32, [None], 'actions')
      self.labels = tf.placeholder(tf.float32, [None], 'labels')
      self.epsilon = tf.placeholder(tf.float32, [], 'epsilon')

    self.layers.append(self.data)

  def _create_conv_layers(self):
    input_ = self.layers[-1]
    for (name, n, size, stride) in self.conv_templates:
      out = Conv2D(name, input_, n, [size, size], stride).to_tf()
      self.layers.append(out)
      input_ = out

  def _create_fc_layers(self):
    input_ = tf.contrib.layers.flatten(self.layers[-1])
    for (name, n) in self.fc_templates:
      out = FC(name, input_, n).to_tf()
      self.layers.append(out)
      input_ = out

  def _add_out(self):
    with tf.variable_scope('output'):
      self.out = FC('out', self.layers[-1], self.nactions, activation_fn=None).to_tf()
      self.best_action = tf.argmax(self.out, dimension=1)
      self.best_reward = tf.reduce_max(self.out, reduction_indices=1)

    self.layers.append(self.out)

  def _add_loss(self):
    with tf.variable_scope('loss'):
      actions_one_hot = tf.one_hot(self.actions, self.nactions, name='actions_one_hot')
      q_estimate = tf.reduce_sum(self.out * actions_one_hot, reduction_indices=1, name='q_estimate')
      delta = tf.sub(self.labels, q_estimate, name='delta')
      # Huber loss
      all_loss = tf.select(
        tf.abs(delta) < DELTA,
        0.5 * tf.square(delta),
        DELTA * (tf.abs(delta) - 0.5 * DELTA),
        name='all_loss'
      )
      self.loss = tf.reduce_mean(all_loss, name='loss')

  def _add_optimizer(self):
    with tf.variable_scope('optimize'):
      self.global_step = tf.Variable(0, name='global_step', trainable=False)
      optimizer = tf.train.AdamOptimizer()
      self.gradients = optimizer.compute_gradients(self.loss)
      self.optimize = optimizer.apply_gradients(self.gradients, global_step=self.global_step)

  def _add_summaries(self):
    with tf.variable_scope('summary'):
      self.terminal_reward = tf.Variable(0., name='terminal_reward', trainable=False)
      self.win = tf.Variable(0., name='win', trainable=False)
      ema = tf.train.ExponentialMovingAverage(decay=0.9)
      self.maintain_averages_op = ema.apply([self.terminal_reward, self.win])

      tf.scalar_summary('loss', self.loss)
      tf.scalar_summary('epsilon', self.epsilon)
      tf.scalar_summary('terminal_reward', ema.average(self.terminal_reward))
      tf.scalar_summary('win', ema.average(self.win))

      batch_best = tf.argmax(self.best_reward, dimension=0)
      tf.scalar_summary('best_reward', tf.gather(self.best_reward, batch_best))
      tf.histogram_summary('best_action', tf.gather(self.best_action, batch_best))

      averaged_out = tf.reduce_mean(self.out, reduction_indices=0)
      for i in range(self.nactions):
        tf.histogram_summary('q[{}]'.format(i), averaged_out[i])

      for grad, var in self.gradients:
        tf.histogram_summary('{}/gradient'.format(var.name), grad)

      self.summaries = tf.merge_all_summaries()

  def save(self):
    self.saver.save(self.session, self.model_file, global_step=self.global_step)

  def set_terminal_reward(self, reward, is_win):
    with tf.control_dependencies([self.terminal_reward.assign(reward), self.win.assign(int(is_win))]):
      op = tf.group(self.maintain_averages_op)
    self.session.run(op)

  def feed_dict(self, data, actions, labels, extra_feed_dict=None):
    feed_dict = {
      self.data: data,
      self.actions: actions,
      self.labels: labels,
    }
    feed_dict.update(extra_feed_dict or {})
    return feed_dict

  def _train(self, ops, feed_dict):
    step = tf.train.global_step(self.session, self.global_step)
    if self.log and step % WRITE_SUMMARY_EVERY == 0:
      ops.append(self.summaries)
    results = self.session.run(ops, feed_dict)
    if self.log and step % WRITE_SUMMARY_EVERY == 0:
      self.writer.add_summary(results.pop(), global_step=step)
    return results

  def train(self, data, actions, labels, extra_feed_dict=None):
    self._train([self.optimize], self.feed_dict(data, actions, labels, extra_feed_dict))

  def train_loss(self, data, actions, labels, extra_feed_dict=None):
    _, loss = self._train([self.optimize, self.loss], self.feed_dict(data, actions, labels, extra_feed_dict))
    return loss

  def eval_best_action(self, data):
    return self.best_action.eval({self.data: [data]}, session=self.session)[0]

  def eval_best_reward(self, data):
    return self.best_reward.eval({self.data: [data]}, session=self.session)[0]

  def to_tf(self):
    return self.out
