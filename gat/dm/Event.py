'''
This class represents an event in an actor's history/memory. It records the state that the actor was in, and the move that was made from that state
'''
class Event:
    def __init__(self, currentState, desiredState, move, success):
        self.currentState = currentState
        self.desiredState = desiredState
        self.move = move
        self.success = success

    '''
    Compute how different two events are based on the state. Equal states will have 0 difference, so compare will return 0.
    '''
    @staticmethod
    def compare(event1, event2):
        return Event.compareResources(event1.state.resources, event2.state.resources)

    #TODO: make dictionary instead of list
    @staticmethod
    def compareResources(a, b):
        difference = 0
        for item in list(a.keys()):
            difference += abs(a.get(item) - b.get(item))
        return difference