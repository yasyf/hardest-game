from deepq import DeepQTrainer
from ...hardest_game.simulator import HardestGameSimulator

def run_main(klass):
  trainer = DeepQTrainer(klass)
  trainer.train()

if __name__ == '__main__':
  run_main(HardestGameSimulator)
