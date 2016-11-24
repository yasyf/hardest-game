from deepq import DeepQTester
from ...toy_game.simulator import ToyGameSimulator

def run_main(klass):
  tester = DeepQTester(klass)
  tester.test()

if __name__ == '__main__':
  run_main(ToyGameSimulator)
