from ..toy_game.replay_memory import ToyGameReplayMemory
from move import ToyGame2DMove as Move

class ToyGame2DReplayMemory(ToyGameReplayMemory):
  def did_move(self):
    return self.action != Move.stay and ((self.next_state.x != self.state.x) or (self.next_state.y != self.state.y))
