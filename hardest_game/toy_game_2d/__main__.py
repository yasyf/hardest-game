from level import Level
from simulator import ToyGame2DSimulator

def run_main():
  level = Level((1, 1), 2)
  with ToyGame2DSimulator(level) as simulator:
    simulator.make_move('right')
    simulator.make_move('down')
    simulator.sample().show()
    print simulator.sample().state.feature_vector()

if __name__ == '__main__':
  run_main()
