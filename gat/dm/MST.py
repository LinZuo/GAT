import networkx as nx


class MST:
    def __init__(self, currentState, desiredState, moves, maxTime):
        self.currentState = currentState
        self.desiredState = desiredState
        self.graph = nx.DiGraph()
        self.maxTime = maxTime
        self.possibleMoves = moves
        self.tree = self.generateTree(self.currentState, 0)

    '''
    build the tree
    parentNode = the current state of the system, which will be the root node of the tree.
    curTime - the amount of time ticks for which to build the tree.
    '''

    def generateTree(self, parentNode, currentTime):
        self.graph.add_node(parentNode)
        if parentNode != self.desiredState:
            for move in self.possibleMoves:
                possibleState = move.getPossibleState(parentNode)
                # possibleState.setTime(currentTime)
                self.graph.add_node(possibleState)
                self.graph.add_edge(parentNode, possibleState, object=move)

        if currentTime < self.maxTime - 1:
            # change this to self.graph.neighbors(parentNode)
            adjacency = self.graph[parentNode]
            for k in list(adjacency):
                self.generateTree(k, currentTime=currentTime + 1)

        return parentNode

    '''
    remove the given move (starting from the curState) from the tree.
    '''

    def removeMove(self, move):
        neighbors = self.graph.neighbors(self.currentState)
        child = None
        for neighbor in neighbors:
            if self.graph.get_edge_data(self.currentState, neighbor)["object"] == move:
                child = neighbor
        if child is not None:
            self.removePath(self.currentState, child)

    '''
    remove a whole path, up until it merges with another existing one or until it reaches the desired state.
    '''

    def removePath(self, parentNode, childNode):
        move = self.graph[parentNode][childNode]['object']
        self.graph.remove_edge(parentNode, childNode)
        self.possibleMoves.remove(move)

    '''
    Get all of the moves from the current state.
    '''

    def getMoves(self):
        return self.possibleMoves

    def containsMove(self, move):
        # checks if move is in neighbors
        edges = [self.graph[self.currentState][childNode]['object'] for childNode in
                 self.graph.neighbors(self.currentState)]
        return move in edges
