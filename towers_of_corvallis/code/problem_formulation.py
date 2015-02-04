import priority_queue as pq
from sets import Set
from copy import deepcopy


class State(object):
    """Define a state as a list of pegs."""
    def __init__(self, pegs):
        self.pegs = pegs
        self.name = str(pegs)
        self.pathcost = 0
        self.heurcost = 0
        self.priority = 0
        self.parent = None

    def __lt__(self, other):
        return (self.pathcost+self.heurcost) <= (other.pathcost+other.heurcost)

    def equal(self, other):
        return self.name == other.name
        
    def goaltest(self, other):
        return self.equal(other)

    def child(self, action):
        pegscopy = deepcopy(self.pegs)
        peg = pegscopy[action[0]]
        pegscopy[action[1]].append(peg.pop())
        newstate = State(pegscopy)
        newstate.pathcost = self.pathcost + 1
        newstate.parent = self
        return newstate
    
    def setpriority(self):
        self.priority = self.pathcost+self.heurcost

    def printself(self):
        print 'pathcost:', self.pathcost
        print 'heurcost:', self.heurcost

class Heuristic(object):
    """Define heuristic function."""
    def cost(self, state, goal):
        pass

class Admissible(Heuristic):
    """Define admissible heuristic function."""
    def cost_bfs(self, state, goal):
        return 0

    def cost(self, state, goal):
        maps = {}
        cost = []
        for i,peg in enumerate(state.pegs):
            for j,disk in enumerate(peg):
                maps[disk] = [(i,j)]
        for i,peg in enumerate(goal.pegs):
            for j,disk in enumerate(peg):
                maps[disk].append((i,j))
        # print maps
        for key,val in maps.iteritems():
            cost.append(self.disktogoal(val[0],val[1],state.pegs))
        return max(cost)

    # The shortest path for moving a disk to its destination.
    def disktogoal(self, diskpos, goalpos, pegs):
        pd = len(pegs[diskpos[0]])
        pg = len(pegs[goalpos[0]])
        cost = 0
        if diskpos[0] != goalpos[0]:
            if pg >= goalpos[1]:
                cost += pg - goalpos[1]
                cost += pd - diskpos[1]
                cost += 1
            else:
                cost += pd - diskpos[1]
                cost += 1
                if (goalpos[1]-pg) > (pd-diskpos[1]):
                    cost += goalpos[1]-pg-(pd-diskpos[1])
        else:
            if diskpos[1] != goalpos[1]:
                cost += 2
                cost += abs(goalpos[1]-diskpos[1])
        return cost


class NonAdmissible(Heuristic):
    """Define admissible heuristic function."""
    def cost(self, state, goal):
        pass


class Astar(object):
    """A star search algorithm."""
    def __init__(self, state, goal, heuristic):
        self.state = state
        self.goal = goal
        self.heuristic = heuristic
        self.state.heurcost = self.heuristic.cost(self.state, self.goal)
        self.state.setpriority()
        self.frontier = pq.PriorityQueue()
        self.frontier.add(self.state)
        self.explored = Set()

    def actions(self, state):
        actions = []
        for i, peg in enumerate(state.pegs):
            # print (i,peg)
            for j in range(len(state.pegs)):
                if (i!=j) and peg:
                    actions.append((i,j))
        # print actions
        return actions

    def search(self):
        while True:
            if self.frontier.isempty():
                print 'There is no any solution.'
                return False
            state = self.frontier.pop()
            print 
            print state.name

            if state.goaltest(self.goal):
                print 'success', state.name
                state.printself()
                self.solution = self.backtrack(state)[::-1]
                return True


            self.explored.add(state.name)
            for act in self.actions(state):
                child = state.child(act)
                child.heurcost = self.heuristic.cost(child, self.goal)
                child.setpriority()
                if child.name not in self.explored:
                    if not self.frontier.contain(child):
                        self.frontier.add(child)
                    elif self.frontier.getpriority(child) > child.priority:
                        self.frontier.setpriority(child)
                # print 'frontier:', self.frontier.entryfinder
                # print 'explored:', self.explored

    def backtrack(self, state):
        sequence  = [state]
        while state.parent is not None:
            sequence.append(state.parent)
            state = state.parent
        return sequence

class RBFS(Astar):
    """Recursive best first search algoritm."""

def test_astar(state, goal):
    heur = Admissible()
    astar = Astar(state,goal,heur)
    astar.search()
    print [i.name for i in astar.solution]

def test_heuristic(state, goal):
    h = Admissible()
    print state.name
    print 'h-cost:', h.cost(state, goal)

if __name__ == '__main__':
    p1 = State([[1,2],[],[]])
    g1 = State([[2,1],[],[]])
    p2 = State([[1,2,3,4],[],[]])
    g2 = State([[],[1,2],[3,4]])
    p3 = State([[1,2,3,4,5,6],[],[]])
    g3 = State([[6,5],[3,4],[1,2]])
    p3 = State([[1,2,3,4,5,6,7],[],[]])
    g3 = State([[6,5,7],[3,4],[1,2]])

    print 'Heuristic Test:'
    test_heuristic(p1,g1)
    test_heuristic(p2,g2)
    test_heuristic(p3,g3)
    print 

    print 'Astar Test:'
    test_astar(p1,g1)
    test_astar(p2,g2)
    test_astar(p3,g3)
    print












