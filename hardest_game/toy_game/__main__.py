from level import Level
from simulator import ToyGameSimulator

def run_main():
  level = Level(1, 2)
  with ToyGameSimulator(level) as simulator:
    simulator.make_move('right')
    simulator.make_move('stay')
    simulator.sample().show()

if __name__ == '__main__':
  run_main()
