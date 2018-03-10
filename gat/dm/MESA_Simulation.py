import sys

sys.path.append("..")
import gat.dm.utils as utils
from gat.dm.Move import Move
from gat.dm.Pole import *
from gat.dm.State import State
from gat.dm.risk_calculation import generate_resource_vocab
from gat.dm.MST import MST
from gat.dm import IO
from gat.dm import risk_calculation
from gat.dm.Event import Event
from mesa import Model
from mesa.time import RandomActivation, BaseScheduler
from gat.dm.Actor_MESA import Actor


# do something else

class Simulator(Model):
    """A model with some number of agents."""

    def __init__(self, N):
        super().__init__(N)
        self.num_agents = N
        self.schedule = RandomActivation(self)
        self.data_collector = None
        self.moves_made = None

        self.add_actor()
        self.add_actor()
        self.add_actor()

    ##############################################################################

    def add_actor(self):
        rationality = RationalityPole(0, 1)
        risk = RiskPole(0, 1)
        emotion = EmotionalPole(0, 1)
        generosity = GenerosityPole(0, 1)
        particularHolistic = ParticularHolisticPole(1, 1)
        primacyRecency = PrimacyRecencyPole(0, 1)
        routineCreative = RoutineCreativePole(0, 1)

        data = utils.read_moves("static/resources/dm_data/moves.csv")
        moves = []
        for move in data:
            IO_string_set = set()

            IO_list = [utils.IO_random_sampler(x) for x in
                       [move["warmth"],
                        move["affinity"], move["legitimacy"],
                        move["dominance"], move["competence"]]]
            IO_string = utils.list_to_string(IO_list)
            while IO_string in IO_string_set:
                IO_list = [utils.IO_random_sampler(x) for x in
                           [move["warmth"],
                            move["affinity"], move["legitimacy"],
                            move["dominance"], move["competence"]]]
            moves.append(Move(move["code"],
                              move["move_name"],
                              move["move_type"],
                              IO_list,
                              move["ph"],
                              [resource.strip() for resource in move["low_resources"].replace(",", " ").split()],
                              [resource.strip() for resource in move["med_resources"].replace(",", " ").split()],
                              [resource.strip() for resource in move["high_resources"].replace(",", " ").split()],
                              move["infrastructure"],
                              category='Build political infrastructure'))

        generate_resource_vocab(moves)
        # TODO
        # one hot for infrastructure as well

        s1 = [1000] * 52
        s2 = [100] * 52
        s3 = [-1000] * 52

        curState = State({i: s1[i] for i in range(len(s1))}, {0: 0})
        desState = State({i: s2[i] for i in range(len(s2))}, {0: 100})
        criticalState = State({i: s3[i] for i in range(len(s3))}, {0: -1000})

        io_values = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0}

        globalresource = Actor(unique_id=0, model=self,
                               poles=[rationality, risk, emotion, generosity, particularHolistic, primacyRecency,
                                      routineCreative],
                               currentState=curState, desiredState=desState, maxTime=2, error=0,
                               history=[], criticalState=criticalState, allActors=[], ioValues=io_values,
                               end_io_state=io_values)
        self.schedule.add(globalresource)

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()

    def multi_step_collector(self, times):
        initial_state = {}
        for a in self.schedule.agents:
            initial_state[a.unique_id] = a.currentState.resources.copy()
        data_collector = []
        data_collector.append(initial_state)
        moves_made = []
        for i in range(times):
            self.step()
            temp_state = {}
            temp_move = {}
            for a in self.schedule.agents:
                temp_state[a.unique_id] = a.currentState.resources.copy()
                temp_move[a.unique_id] = a.moves_made
            data_collector.append(temp_state)
            moves_made.append(temp_move)
        return data_collector, moves_made

    def watcher(self, times, agent_alert=[], resources_alert={}, moves_alert=[]):  # three conditions in total
        initial_state = {}
        for a in self.schedule.agents:
            initial_state[a.unique_id] = a.currentState.resources.copy()
        data_collector = []
        data_collector.append(initial_state)
        moves_made = []
        for i in range(times):
            self.step()
            temp_state = {}
            temp_move = {}

            for a in self.schedule.agents:
                temp_state[a.unique_id] = a.currentState.resources.copy()
                temp_move[a.unique_id] = a.moves_made

                # one condition
                if a.unique_id in agent_alert and len(resources_alert) == 0 and len(moves_alert) == 0:
                    yield ' '.join(
                        ('the moves that actor', str(a.unique_id), 'made at step', str(i + 1), 'is', str(a.moves_made)))
                    yield ' '.join(
                        ('the resources of actor', str(a.unique_id), 'made at step', str(i + 1), 'is',
                         str(a.currentState.resources)))
                if len(moves_alert) != 0 and len(agent_alert) == 0 and len(resources_alert) == 0:
                    for m in moves_alert:
                        if m in [str(e) for e in a.moves_made]:
                            yield ' '.join(('actor', str(a.unique_id), 'made the move', str(m), 'at step', str(i + 1)))
                if len(resources_alert) != 0 and len(agent_alert) == 0 and len(moves_alert) == 0:
                    for r in resources_alert.keys():
                        if a.currentState.resources[r] == resources_alert[r]:
                            yield ' '.join(
                                (
                                'the resources', str(r), 'of actor', str(a.unique_id), 'reach', str(resources_alert[r]),
                                'at step',
                                str(i + 1)))

                # two conditions
                if a.unique_id in agent_alert and len(resources_alert) != 0:
                    for r in resources_alert.keys():
                        if a.currentState.resources[r] == resources_alert[r]:
                            yield ' '.join(
                                (
                                'the resources', str(r), 'of actor', str(a.unique_id), 'reach', str(resources_alert[r]),
                                'at step',
                                str(i + 1)))
                if len(moves_alert) != 0 and a.unique_id in agent_alert:
                    for m in moves_alert:
                        if m in [str(e) for e in a.moves_made]:
                            yield ' '.join(('actor', str(a.unique_id), 'made the move', str(m), 'at step', str(i + 1)))

            data_collector.append(temp_state)
            moves_made.append(temp_move)
        self.data_collector = data_collector
        self.moves_made = moves_made
        yield 'simulation done!'

# empty_model = Simulator(N=1)
# data, moves=empty_model.multi_step_collector(20)
# data, moves = empty_model.watcher(100, agent_alert=[1], resources_alert={5: 31}, moves_alert=['Threaten'])
