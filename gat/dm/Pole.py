import abc
import pickle
import random

import numpy as np

from gat.dm.Actor import Event

'''
This is the superclasss for all poles. Classes inheriting from this class must define a method act.
'''


class Pole(object, metaclass=abc.ABCMeta):
    def __init__(self, value, weight):
        self.value = value
        self.weight = weight

    @abc.abstractmethod
    def actOnMST(self, mst, actor):
        return

    @abc.abstractmethod
    def actOnList(self, orderedList, actor):
        return


'''
The following classes inherit from the Pole superclass above. They all must define a method act. Whenever there is an error term used, this should be the actor.error.
'''


class RationalityPole(Pole):
    def __init__(self, value, weight):
        super(RationalityPole, self).__init__(value, weight)

    def actOnList(self, orderedList, actor):

        nl = sorted(orderedList, key=lambda x: x.sum)
        tempval = round(len(nl) * ((self.value + 1) / 2.0 + actor.error))
        ol = orderedList[:tempval]

        return ol

    def actOnMST(self, mst, actor):
        # rationality: a more rational actor will consider moves that have a higher probability of ending up in the desired state
        moves = mst.getMoves()  # get all moves avaliable from current state
        movelist = moves[:]
        val = (self.value + 1) / 2.0 - actor.error
        for move in movelist:
            if move.probability < ((self.value + 1) / 2.0 - actor.error):
                # remove the moves that have a probability of ending up in the desired state lower than the actor's rationality + an error term
                # im assuming that the probability of ending up in the desired state is the value of tbe move  and the value of the pole is the actors rationality
                # make sure move and probability are on similar scales
                # error increases rationality
                mst.removeMove(move)
        return mst


class RiskPole(Pole):
    def __init__(self, value, weight):
        super(RiskPole, self).__init__(value, weight)

    def actOnList(self, orderedList, actor):
        # risk: allow moves for which there aren't enough resources
        # this increases the error term for the resource cut
        # done proportional to the pole. If the pole is 100%, the error term will go to infinity and no moves will be filtered by the resource cut
        orderedMoves = orderedList
        actor.resourcesError = (self.value + 1) / 2
        return orderedMoves

    def actOnMST(self, mst, actor):
        # risk: a more risky actor will consider moves that have a higher risk associated with them
        # work with mst
        moves = mst.getMoves()  # get all moves available from current state
        moves = moves[:]
        temp = max([v for k, v in list(actor.currentState.resources.items())])
        for move in moves:
            if move.risk > (((
                                         self.value + 1) / 2.0) + actor.error) * temp:  # remove all moves that have a higher risk than the value of the pole + an error term with mst.removeMove(move)

                # risk and probability and error are on similar scales
                # error decreases risk
                mst.removeMove(move)
        return mst


class ParticularHolisticPole(Pole):
    # stubbornness will be stubborn, want to do specifically what the previous poles chose, and disregard what poles later say
    def __init__(self, value, weight):
        super(ParticularHolisticPole, self).__init__(value, weight)

    def actOnList(self, orderedList, actor):
        # holistic vs particular: holistic actor considers moves further from centroid.
        # work with list of orderedMoves from k-means
        orderedMoves = sorted(orderedList, key=lambda move: abs(
            np.linalg.norm(np.subtract(move.ioValues, list(actor.ioValues.values())))))
        # obtain greatest possible distance from centroid
        maxdistance = abs(np.linalg.norm(np.subtract(orderedMoves[-1].ioValues, list(actor.ioValues.values()))))

        # scale the value of the particular/holistic pole by that amount.
        tempval = maxdistance * ((self.value + 1) / 2.0 + actor.error)
        # return moves that are a distance less than or equal to the scaled pole value + an error term from the orderedMoves list

        orderedMoves = [move for move in orderedMoves if
                        abs(np.linalg.norm(np.subtract(move.ioValues, list(actor.ioValues.values())))) <= (tempval)]
        # what is error value
        return orderedMoves

    def actOnMST(self, mst, actor):
        # stubbornness will be stubborn, want to do specifically what the previous poles chose, and disregard what poles later say, what are we saying here?
        # 100% stubborn actor will not proceed to any pole later on. less stubborn actors will let more poles act.
        tempval = (self.value + 1) / 2.0
        actor.polesLeft = actor.polesLeft[:int(round(tempval * len(actor.polesLeft)))]
        return mst


class PrimacyRecencyPole(Pole):
    def __init__(self, value, weight):
        super(PrimacyRecencyPole, self).__init__(value, weight)

    def actOnMST(self, mst, actor):
        # primacy (#using history as a guideline) vs recency (being more creative : go through actor's history/memory (in a way that is reflective of the value of the pole, ie if the actor likes history more, then more events in history will be considered and vice versa)
        # need to be careful about removing too many moves. Juan check it so it doesn't remove everything
        # still need to make sure that we are not removing every move
        # history = actor.history
        # memory = actor.memory
        # moves = mst.getMoves()
        # value = abs(self.value)
        # compPv = 1 - value
        # combMoves = []
        # if self.value < 0: #go into primacy
        #     hisMoves = history[:int(value*len(history))]
        #     memMoves = memory[:int(compPv*len(memory))]
        #     combMoves = hisMoves.append(memMoves) #contains both the moves in memory and the moves in history that will be looked at
        # if self.value >= 0: #go into recency
        #     hisMoves = history[:int(compPv*len(history))]
        #     memMoves = memory[:int(value*len(memory))]
        #     combMoves = hisMoves.append(memMoves)
        #
        # temp = max([v for k,v in actor.currentState.resources.items()])
        # for sim in combMoves:
        #     hisSimilarity = Event.compareResources(actor.currentState.resources, sim.resources)
        #     if (hisSimilarity < (self.value + actor.error) * temp and hisSimilarity > (self.value - actor.error) * temp):  # if a state in history is similar enough (within error bound) to the actor's current state:
        #         for move in moves:
        #             moveSimilarity = Event.compareResources(move.resources, sim.resources)
        #             if (moveSimilarity > (self.value + actor.error) * temp  or moveSimilarity < (self.value - actor.error)):# if the move taken then is not similar enough (outside error bound) to a move in the MST, then remove it from MST.
        #                 mst.removeMove(move)
        #
        #     # need to be careful about removing too many moves. Juan check it so it doesn't remove everything
        if self.value < 0:  # TODO ask if we want to change the important one because its removing
            important = actor.memory
            other = actor.history
        else:
            important = actor.history
            other = actor.memory
        value = int(abs(self.value) * min(len(actor.history), len(actor.memory))) if self.value is not 0 else 1
        otherCount = 0
        for importantCount in range(1, len(important) + 1):

            self.removefromTree(important[importantCount - 1], mst, actor)
            if importantCount % value == 0:
                self.removefromTree(other[otherCount], mst, actor)
                otherCount += 1

        return mst

    def removefromTree(self, element, mst, actor):

        error = actor.error * max([v for k, v in list(actor.currentState.resources.items())])
        similarity = Event.compareResources(element.move.resources, actor.currentState.resources)

        if similarity > error:
            if mst.containsMove(element.move):
                mst.removeMove(element.move)

    # def actOnList(self, orderedList, actor):
    #     history = actor.history
    #     memory = actor.memory
    #     val = int(round(abs((1 - self.value)/self.value))) if self.value != 0 else 0
    #     error = actor.error * max([resource for resource in actor.currentState.resources])
    #     simMovesSet = set()
    #     for event in history:
    #         splice = memory[:val]
    #         hisSimilarity = Event.compareResources(event.currentState.resources, actor.currentState.resources)
    #         for item in splice:
    #             memSimilarity = Event.compareResources(item.move.resources, actor.currentState.resources)
    #             if(hisSimilarity < error):
    #                 simMovesSet.add(event)
    #             elif(memSimilarity < error):
    #                 simMovesSet.add(item)
    #     updatedMoves = orderedList.append(list(simMovesSet))
    #     return updatedMoves

    def actOnList(self, orderedList, actor):
        if self.value < 0:
            important = actor.memory
            other = actor.history
        else:
            important = actor.history
            other = actor.memory
        value = abs(self.value) * min(len(actor.history), len(actor.memory)) if self.value is not 0 else 1
        otherCount = 0
        addition = set()
        for importantCount in range(0, len(important)):
            self.addToSet(important[importantCount], addition, actor)
            if importantCount % value == 0:
                self.addToSet(other[0], addition, actor)
                otherCount += 1

        updatedMoves = orderedList
        updatedMoves += (list(addition))
        return updatedMoves

    def addToSet(self, element, addition, actor):
        error = actor.error * max([v for k, v in list(actor.currentState.resources.items())])
        similarity = Event.compareResources(element.move.resources, actor.currentState.resources)
        if similarity < error:
            addition.add(element.move)


class RoutineCreativePole(Pole):
    def __init__(self, value, weight):
        super(RoutineCreativePole, self).__init__(value, weight)

    def actOnMST(self, mst, actor):
        # routine vs creative: creative actor considers more random moves.
        moves = mst.getMoves()  # get all moves available from current state
        moves = moves[:]
        for move in moves:  # for every move going from the current state:
            rnum = random.uniform(0,
                                  1)  # do you think numpy is better at this? -- obtain a random number within bounds [0, 1). if it is more than the value of the routine/creative pole + an error Term:
            if rnum > ((self.value + 1) / 2.0 - actor.error):
                mst.removeMove(move)  # path will be removed. via mst.removeMove
        return mst

    # todo: this function will remove all moves if they are routine// unless you scale the value to be between 0 and 1 ask nikita

    def actOnList(self, orderedList, actor):
        # routine vs creative: routine actor will consider moves that have been successful in the past, while creative actors will be willing to try new moves
        # Add successful moves from the past to the list (Not all successful moves, only maxTimeTicks amount of moves in the past). Most successful moves will be added first.
        # success of a move is defined in actor.howSuccessfulWasMove
        # go through the list, removing moves that are not similar enough to the successful moves
        # how similar enough depends on the value of the pole: 100% creative actor will have no moves removed. -1 is routine, 1 is creative

        orderedMoves = orderedList
        oldMoves = actor.successfulMoves[:actor.timeTicks]

        orderedMoves += [event.move for event in oldMoves]
        # only want to remove if you are routine, need to scale based on pole values
        addition = set()

        if len(actor.successfulMoves) <= 10:
            return orderedMoves

        for move in orderedMoves:
            # find the most similar move in actor.successful moves
            # if that move is still not similar enough, then remove it
            # similar enough = same way we did up there

            for event in actor.successfulMoves:
                sim = Event.compareResources(move.resources, event.move.resources)
                error = actor.error * max([v for k, v in list(actor.currentState.resources.items())])
                rnum = random.random()
                if sim < error and rnum <= (self.value + 1) / 2:
                    addition.add(move)
                    break

        updatedMoves = list(addition)

        return updatedMoves


class EmotionalPole(Pole):
    def __init__(self, value, weight):
        super(EmotionalPole, self).__init__(value, weight)

        with open('./static/resources/dm_data/EmotionalPoleCategories', 'rb') as file:
            self.moveCategories = pickle.load(file)

    # positive love negative fear 0 bland
    # extreme values are error terms

    def actOnList(self, orderedList, actor):
        # see below for description of pole function.
        # add moves that go along with the value of the pole, similar to the way they are removed below.
        orderedMoves = orderedList
        poleVal = self.value
        actError = actor.error
        if poleVal < -0.8:
            actError += 1 - abs(self.value)  # just reset the error? or add the difference
        if poleVal > 0.8:
            # set error term
            actError += 1 - self.value
        movToBeAdded = set()
        upperBound = min(poleVal + actError, 1)
        lowerBound = max(poleVal - actError, -1)
        for move in actor.history:
            if (np.mean(self.moveCategories.get(move.move.category)) > lowerBound and np.mean(self.moveCategories.get(
                    move.move.category)) < upperBound):  # how to pick a value if the move category values have multiple values?
                movToBeAdded.add(move.move)
        updatedMoves = orderedMoves + list(movToBeAdded)
        return updatedMoves

    def actOnMST(self, mst, actor):
        # anything beyond -0.8 or 0.8 (extreme) we treat as increased error and in this case, tendency to choose violence.
        # From 0 to 0.7 you have increased tendency to build
        # From 0 to -0.7 you have a tendency to destroy. This is manifested through increasingly hostile kinetic moves.
        # go through MST. check category of move through move.category
        # moveCategories = a dictionary mapping from category to a range of values of this pole. <- will be given somehow. Depends on SMRs.
        # remove moves whose category does not map to a range of values that contains the value of the pole (+/- an arror term)

        poleVal = self.value
        err = actor.error
        if poleVal < -0.8:
            err += 1 - abs(self.value)
        if poleVal > 0.8:
            err += 1 - self.value
        upperBound = min(poleVal + err, 1)
        lowerBound = max(poleVal - err, -1)
        moves = mst.getMoves()
        moves = moves[:]

        if lowerBound != upperBound:
            for move in moves:

                if not (np.mean(self.moveCategories.get(move.category)) > lowerBound and np.mean(
                        self.moveCategories.get(move.category)) < upperBound):
                    mst.removeMove(move)

        return mst


class GenerosityPole(Pole):
    def __init__(self, value, weight):
        super(GenerosityPole, self).__init__(value, weight)
        self.maxListPrice = None

    def actOnList(self, orderedList, actor):
        orderedMoves = orderedList
        if self.maxListPrice == None:
            self.maxListPrice = 0  # if self.maxListPrice = None: (if statement for caching)
            for move in orderedMoves:  # go through list, find most expensive move by summing over all resources. self.maxListPrice = resulf of this calculation
                if self.maxListPrice < move.sum:
                    self.maxListPrice = move.sum

        scaledVal = (((self.value + actor.error) + 1) / 2) * self.maxListPrice

        orderedMoves = [x for x in orderedMoves if x.sum <= (scaledVal)]
        return orderedMoves

    def actOnMST(self, mst, actor):

        moves = mst.getMoves()
        moves = moves[:]
        mostExpensiveMove = max([move.sum for move in moves])  # figure this out
        # first time find most expensive move = val
        scaledVal = ((self.value + 1) / 2) * mostExpensiveMove  # Pole Scaling and Val are calculated at the same time
        # scale pole to [0, 1]
        # val = val * most expensive move

        for move in moves:
            if move.sum > scaledVal:
                mst.removeMove(move)

        return mst
