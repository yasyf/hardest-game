from __future__ import print_function, division
from level import Level
from move import Move
from property import Property
from scipy.misc import imread
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from sample import Sample
from state import State
from util import static_dir, to_enum, waitable
import time, tempfile, os

SAUCE_USERNAME = os.getenv('SAUCE_USERNAME')
SAUCE_KEY = os.getenv('SAUCE_KEY')
SWFPATH = static_dir('swf', 'worlds-hardest-game.swf')
SWFURL = 'http://www.worldshardestgame.org/files/worlds-hardest-game.swf'
MOVE_DISTANCE = 4
ANIMATION_DELAY = 0.05
BASE_FRAME = 60

class GameError(Exception):
  pass

class Simulator(object):
  def __init__(self, name='Simulator', time_step=0.1, verbose=True, moves=None, use_remote=False):
    self.name = name
    self.steps = int(time_step / ANIMATION_DELAY)
    self.verbose = verbose
    self.moves = moves or []
    if use_remote is None:
      self.use_remote = SAUCE_USERNAME and SAUCE_KEY
    else:
      self.use_remote = use_remote
    self.driver = self.new_driver()

  def new_driver(self):
    if self.use_remote:
      self.log('using remote driver')
      capabilities = {
        'browserName': 'MicrosoftEdge',
        'platform': 'Windows 10',
        'version': '14',
        'screenResolution': '1024x768',
      }
      url = 'http://{}:{}@ondemand.saucelabs.com:80/wd/hub'.format(SAUCE_USERNAME, SAUCE_KEY)
      return webdriver.Remote(desired_capabilities=capabilities, command_executor=url)
    else:
      self.log('using local driver')
      options = Options()
      options.add_argument('--always-authorize-plugins=true --mute-audio=true')
      return webdriver.Chrome(chrome_options=options)

  def log(self, *args):
    if self.verbose:
      print('[{}]: {}'.format(self.name, ' '.join(map(str, args))))

  def click_at(self, pos, after=1):
    self.log('sleeping', after)
    time.sleep(after)
    self.log('clicking', pos)
    body = self.driver.find_element_by_tag_name('body')
    chain = webdriver.ActionChains(self.driver).move_to_element_with_offset(body, *pos).click()
    chain.perform()

  def start(self):
    if self.use_remote:
      path = SWFURL
    else:
      path = 'file://{}'.format(SWFPATH)
    self.driver.get(path)
    self.driver.get(path) # yes, we have to load it twice to appease Chrome

    self.play()
    time.sleep(4)

    moves, self.moves = self.moves, []
    self.make_moves(moves)

  def quit(self):
    try:
      self.driver.close()
    except:
      pass

  def __enter__(self):
    self.start()
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    self.quit()

  def __del__(self):
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

  @waitable
  def get_property(self, target, property):
    return self._execute('TGetProperty', '/' + target, Property[property])

  def set_property(self, target, property, value):
    return self._execute('TSetProperty', '/' + target, Property[property], value)

  @waitable
  def get_variable(self, name):
    return self._execute('GetVariable', name)

  def set_variable(self, name, value):
    return self._execute('SetVariable', name, value)

  @property
  def frame(self):
    return self._execute('TCurrentFrame', '/')

  @frame.setter
  def frame(self, frame):
    return self._execute('TGotoFrame', '/', frame)

  @property
  def level(self):
    return Level.load_or_gen(self.get_variable('currentLevel'), self)

  @level.setter
  def level(self, level):
    self.set_variable('currentLevel', level)
    self.frame = BASE_FRAME + level

  @property
  def coins(self):
    return int(self.get_variable('currentCoins'))

  @property
  def deaths(self):
    return int(self.get_variable('deaths'))

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

  @property
  def state(self):
    return State(self.x, self.y, self.coins, self.level, self.deaths, self.moves)

  def _move_by(self, x, y):
    dx, dy = (x / self.steps), (y / self.steps)
    for _ in range(self.steps):
      self.x += dx
      self.y += dy
      time.sleep(ANIMATION_DELAY)

  def make_move(self, move):
    move = to_enum(move, Move)
    if move == Move.up:
      self._move_by(0, -MOVE_DISTANCE)
    elif move == Move.down:
      self._move_by(0, MOVE_DISTANCE)
    elif move == Move.left:
      self._move_by(-MOVE_DISTANCE, 0)
    elif move == Move.right:
      self._move_by(MOVE_DISTANCE, 0)
    elif move == Move.stay:
      pass
    else:
      raise ValueError(move)

    self.moves.append(move)

    if self.deaths > 0:
      raise GameError('died!')

  def make_moves(self, moves):
    for move in moves:
      self.make_move(move)

  def capture(self):
    with tempfile.NamedTemporaryFile(suffix='.png') as image:
      self.log('capturing', image.name)
      self.driver.get_screenshot_as_file(image.name)
      return imread(image.name, mode='RGB')

  def sample(self, use_cached=True):
    if use_cached:
      return Sample.load_or_gen(self.state.id(), self)
    else:
      return Sample.gen(self.state.id(), self)
