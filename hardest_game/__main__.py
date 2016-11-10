from simulator import Simulator
from move import Move

def run_main():
  simulator = Simulator()
  simulator.start()
  simulator.make_move(Move.up)
  simulator.make_move(Move.up)
  simulator.make_move(Move.up)
  import pdb; pdb.set_trace()

if __name__ == '__main__':
  run_main()
