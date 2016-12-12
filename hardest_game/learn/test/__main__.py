from deepq import DeepQTester
from greedy import GreedyTester
from rand import RandomTester
# from ...toy_game.simulator import ToyGameSimulator
# from ...toy_game_2d.simulator import ToyGame2DSimulator
from ...toy_game_2d_hard.simulator import ToyGame2DHardSimulator

def run_deep(klass):
  tester = DeepQTester(klass)
  tester.test()

def run_greedy(klass):
  tester = GreedyTester(klass)
  tester.test()

def run_random(klass):
  tester = RandomTester(klass)
  tester.test()

if __name__ == '__main__':
  # run_deep(ToyGame2DSimulator)
  # run_greedy(ToyGame2DHardSimulator)
  run_random(ToyGame2DHardSimulator)
