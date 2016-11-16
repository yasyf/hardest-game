from .simulator import Simulator
from multiprocessing import Process, Queue

class SimulatorProcess(Process):
  def __init__(self, i, kwargs, queue):
    Process.__init__(self)
    self.simulator = Simulator(name='Simulator {}'.format(i), **kwargs)
    self.queue = queue

  def run(self):
    self.simulator.start()
    try:
      while True:
        (method, args, kwargs) = self.queue.get(True)
        getattr(self.simulator, method)(*args, **kwargs)
    except:
      self.simulator.quit()

class SimulatorPool(object):
  def __init__(self, size=10, **kwargs):
    self.size = size
    self.init_threads(kwargs)

  def init_threads(self, kwargs):
    self.queues = [Queue() for _ in range(self.size)]
    self.threads = [SimulatorProcess(i, kwargs, self.queues[i]) for i in range(self.size)]

    for thread in self.threads:
      thread.start()

  def quit(self):
    self.run_on_all('quit')

  def run_on_all(self, method, *args, **kwargs):
    for queue in self.queues:
      queue.put_nowait((method, args, kwargs))
