import numpy as np

from gat.dm.State import State


class Move(State):
    def __init__(self, code, move_name, move_type, IO_list,
                 ph, low_resources, med_resources,
                 high_resources, infrastructure, category):
        self.category = category
        self.code = code
        self.move_name = move_name
        self.move_type = move_type
        self.IO = IO_list
        self.ioValues = self.IO
        self.ph = ph
        self.resourcesCategories = {"low": low_resources,
                                    "med": med_resources,
                                    "high": high_resources}

        self.infrastructure = infrastructure
        self.probability = -1  # unassigned
        self.risk = -1  # unassigned
        self._one_hot = []
        self.sum = 0
        self.resources = self.one_hot
        for value in self.one_hot:
            self.sum += value

        super().__init__(self.resources, infrastructure)

    @property
    def one_hot(self):
        return self._one_hot

    @one_hot.setter
    def one_hot(self, val):
        self._one_hot = val
        self.resources = val

    def __str__(self):
        return self.move_name

    __repr__ = __str__

    def getPossibleState(self, curState):
        resources = {}
        for i in curState.resources:
            resources[i] = curState.resources[i] - self.resources[i]

        infrastructure = {}
        # TODO turn this on once infrastructure is fixed
        '''
        for i in curState.infrastructure:
            infrastructure[i] = curState.infrastructure[i] - self.infrastructure[i]
            '''
        return State(resources, infrastructure)

    def compare(self, other):
        return np.sum([abs(self.resources[i] - other.resources[i]) for i in range(0, len(self.resources))])

    def get_IO(self):
        return self.IO

    def get_code(self):
        return self.code

    def get_move_name(self):
        return self.move_name

    def get_move_type(self):
        return self.move_type

    def get_resources(self):
        return self.resources

    def get_infrastructure(self):
        return self.infrastructure

    def to_dic(self):
        move_dic = {"code": self.code,
                    "IO": self.IO,
                    "move_name": self.move_name,
                    "move_type": self.move_type,
                    "ph": self.ph,
                    "resources": self.resources,
                    "infrastructure": self.infrastructure}
        return move_dic
