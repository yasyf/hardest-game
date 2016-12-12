import matplotlib.pyplot as plt
import time

class TestAgentMixin:
  def _show(self):
    plt.ion()
    time.sleep(0.5)
    self.history.get().show(ion=True)
    time.sleep(0.5)
