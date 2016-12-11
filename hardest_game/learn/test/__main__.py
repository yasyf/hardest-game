from deepq import DeepQTester
# from ...toy_game.simulator import ToyGameSimulator
from ...toy_game_2d.simulator import ToyGame2DSimulator

def run_main(klass):
  tester = DeepQTester(klass)
  tester.test()

if __name__ == '__main__':
  run_main(ToyGame2DSimulator)
