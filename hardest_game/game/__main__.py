from simulator import Simulator
from move import Move

def run_main():
  with Simulator(moves=[Move.up] * 5) as simulator:
    for i in range(5):
      simulator.make_move(Move.down)
    for i in range(5):
      simulator.make_move(Move.right)
    sample = simulator.sample()
    sample.show()

if __name__ == '__main__':
  run_main()
