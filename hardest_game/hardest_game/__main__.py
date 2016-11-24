from simulator import HardestGameSimulator
from ..shared.simulator_pool import SimulatorPool
from move import HardestGameMove as Move

def run_sim():
  with HardestGameSimulator(moves=[Move.up] * 5) as simulator:
    for i in range(5):
      simulator.make_move(Move.down)
    for i in range(5):
      simulator.make_move(Move.right)
    sample = simulator.sample()
    sample.show()

def run_pool():
  pool = SimulatorPool(HardestGameSimulator, size=2, moves=[Move.up] * 5)
  pool.run_on_all('make_move', Move.down)
  pool.quit()

if __name__ == '__main__':
  run_pool()
