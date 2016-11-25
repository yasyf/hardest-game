from level import Level
from simulator import ToyGameSimulator
from history import ToyGameHistory

def run_main():
  level = Level(1, 2)
  with ToyGameSimulator(level) as simulator:
    simulator.make_move('right')
    simulator.make_move('left')
    simulator.sample().show()
    print simulator.sample().state.feature_vector()

    history = ToyGameHistory()
    for _ in range(ToyGameHistory.HISTORY_SIZE):
      simulator.make_move('stay', raise_on_death=True)
      history.add(simulator.sample(use_cached=False))
    print history.data

if __name__ == '__main__':
  run_main()
