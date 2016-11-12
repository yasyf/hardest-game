from simulator import Simulator
from move import Move

def run_main():
  with Simulator(history=[Move.up] * 5) as simulator:
    for i in range(5):
      simulator.make_move(Move.down)
    for i in range(5):
      simulator.make_move(Move.right)

if __name__ == '__main__':
  run_main()
