from __future__ import print_function, division
import os, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from move import Move
from property import Property

SWFPATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'static', 'swf', 'worlds-hardest-game.swf'))
MOVE_DISTANCE = 5
ANIMATION_DELAY = 0.1

class Simulator(object):
  def __init__(self, time_step=0.3, verbose=True, history=None):
    self.steps = int(time_step / ANIMATION_DELAY)
    self.verbose = verbose
    self.history = history or []
    self.driver = self.new_driver()

  @staticmethod
  def new_driver():
    options = Options()
    options.add_argument('--always-authorize-plugins=true --mute-audio=true')
    return webdriver.Chrome(chrome_options=options)

  def log(self, *args):
    if self.verbose:
      print('[Simulator]: {}'.format(' '.join(map(str, args))))

  def click_at(self, pos, after=1):
    self.log('sleeping', after)
    time.sleep(after)
    self.log('clicking', pos)
    body = self.driver.find_element_by_tag_name('body')
    chain = webdriver.ActionChains(self.driver).move_to_element_with_offset(body, *pos).click()
    chain.perform()

  def start(self):
    path = 'file://{}'.format(SWFPATH)
    self.driver.get(path)
    self.driver.get(path) # yes, we have to load it twice to appease Chrome

    self.play()
    time.sleep(4)

    moves, self.history = self.history, []
    self.make_moves(moves)

  def quit(self):
    self.driver.close()

  def __enter__(self):
    self.start()
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    self.quit()

  def _execute(self, fn, *args):
    argstr = ['"{}"'.format(arg) for arg in args]
    script = '{fn}({args})'.format(fn=fn, args=', '.join(argstr))
    self.log('executing', script)
    return self.driver.execute_script("return window.document.getElementsByTagName('embed')[0].{}".format(script))

  def play(self):
    self._execute('Play')

  def pause(self):
    self._execute('StopPlay')

  def get_property(self, target, property, wait=True):
    while True:
      value = self._execute('TGetProperty', '/' + target, Property[property])
      if not wait or value is not None:
        return value
      time.sleep(ANIMATION_DELAY)

  def set_property(self, target, property, value):
    return self._execute('TSetProperty', '/' + target, Property[property], value)

  @property
  def x(self):
    return float(self.get_property('player', 'x'))

  @x.setter
  def x(self, x):
    return self.set_property('player', 'x', x)

  @property
  def y(self):
    return float(self.get_property('player', 'y'))

  @y.setter
  def y(self, y):
    return self.set_property('player', 'y', y)

  def _move_by(self, x, y):
    dx, dy = (x / self.steps), (y / self.steps)
    for _ in range(self.steps):
      self.x += dx
      self.y += dy
      time.sleep(ANIMATION_DELAY)

  def make_move(self, move):
    self.history.append(move)
    if move == Move.up:
      self._move_by(0, -MOVE_DISTANCE)
    elif move == Move.down:
      self._move_by(0, MOVE_DISTANCE)
    elif move == Move.left:
      self._move_by(-MOVE_DISTANCE, 0)
    elif move == Move.right:
      self._move_by(MOVE_DISTANCE, 0)
    else:
      raise ValueError(move)

  def make_moves(self, moves):
    for move in moves:
      self.make_move(move)
