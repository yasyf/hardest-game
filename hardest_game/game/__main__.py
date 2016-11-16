from simulator import Simulator
from simulator_pool import SimulatorPool
from move import Move

def run_sim():
  with Simulator(moves=[Move.up] * 5) as simulator:
    for i in range(5):
      simulator.make_move(Move.down)
    for i in range(5):
      simulator.make_move(Move.right)
    sample = simulator.sample()
    sample.show()

def run_pool():
  pool = SimulatorPool(size=2, moves=[Move.up] * 5)
  pool.run_on_all('make_move', Move.down)

if __name__ == '__main__':
  run_pool()
