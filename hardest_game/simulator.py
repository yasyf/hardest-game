from __future__ import print_function, division
import os, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from move import Move
from property import Property

SWFPATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'static', 'swf', 'worlds-hardest-game.swf'))
START_BUTTON = (615, 320)
START_GAME_BUTTON = (130, 500)
BEGIN_BUTTON = (700, 600)
MOVE_DISTANCE = 5
ANIMATION_DELAY = 0.1

class Simulator(object):
  def __init__(self, time_step=0.3, verbose=True):
    self.steps = int(time_step / ANIMATION_DELAY)
    self.verbose = verbose
    self.history = []
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

    self.click_at(START_BUTTON)
    self.click_at(START_GAME_BUTTON, after=9)
    self.click_at(BEGIN_BUTTON)

    time.sleep(2)

  def _execute(self, script):
    self.log('executing', script)
    return self.driver.execute_script("return window.document.getElementsByTagName('embed')[0].{}".format(script))

  def get_property(self, target, property, wait=True):
    while True:
      value = self._execute("TGetProperty('/{}', {})".format(target, Property[property]))
      if not wait or value is not None:
        return value
      time.sleep(ANIMATION_DELAY)

  def set_property(self, target, property, value):
    return self._execute("TSetProperty('/{}', {}, {})".format(target, Property[property], value))

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
    if move == Move.up:
      self._move_by(0, -MOVE_DISTANCE)
