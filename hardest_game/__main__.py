from simulator import Simulator
from move import Move

def run_main():
  with Simulator() as simulator:
    simulator.make_move(Move.up)
    simulator.make_move(Move.up)
    simulator.make_move(Move.up)

if __name__ == '__main__':
  run_main()
