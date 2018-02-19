from gat.dm.MESA_Simulation import Simulator
from threading import Thread, Lock


class DMRunner(Thread):
    message_lock = Lock()
    messages = []

    def __init__(self,
                 number_of_runs=1,
                 steps=100,
                 agent_alert=[1],
                 resources_alert={5: 31},
                 moves_alert=['Threaten']):
        self.number_of_runs = number_of_runs
        self.steps = steps
        self.agent_alert = agent_alert
        self.resources_alert = resources_alert
        self.moves_alert = moves_alert
        super().__init__()

    def run(self):
        for i in range(self.number_of_runs):
            info_str = 'Run {}/{} started'.format((i + 1), self.number_of_runs)
            self.message_lock.acquire()
            self.messages.append(info_str)
            self.message_lock.release()
            empty_model = Simulator(N=1)
            for message in empty_model.watcher(self.steps,
                                               agent_alert=self.agent_alert,
                                               resources_alert=self.resources_alert,
                                               moves_alert=self.moves_alert):
                self.message_lock.acquire()
                self.messages.append(message)
                self.message_lock.release()
            info_str = 'Run {}/{} finished'.format((i + 1), self.number_of_runs)
            self.message_lock.acquire()
            self.messages.append(info_str)
            self.message_lock.release()
        self.message_lock.acquire()
        self.messages.append('###ALL FINISHED###')
        self.message_lock.release()
