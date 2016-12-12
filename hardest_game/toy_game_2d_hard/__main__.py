from simulator import ToyGame2DHardSimulator

def run_main():
  with ToyGame2DHardSimulator() as simulator:
    for move in ['right', 'down', 'down', 'down', 'down', 'right', 'right']:
      simulator.make_move(move, raise_on_death=True)
      simulator.sample().show()
    print simulator.sample().state.feature_vector()

if __name__ == '__main__':
  run_main()
