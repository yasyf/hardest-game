from deepq import DeepQTrainer
from ...hardest_game.simulator import HardestGameSimulator
from ...toy_game.simulator import ToyGameSimulator

def run_main(klass, **kwargs):
  trainer = DeepQTrainer(klass, **kwargs)
  trainer.train()

if __name__ == '__main__':
  # run_main(HardestGameSimulator)
  run_main(ToyGameSimulator, num_steps=1e2)
