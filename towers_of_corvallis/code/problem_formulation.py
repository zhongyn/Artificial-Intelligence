from priority_queue import *
from sets import Set
from copy import deepcopy
import heapq

class State(object):
    """Define a state as a list of pegs."""
    def __init__(self, pegs):
        self.pegs = pegs
        self.name = str(pegs)
        self.heurcost = 0

    def equal(self, other):
        return self.name == other.name
        
    def goaltest(self, other):
        return self.equal(other)
    

class Node(object):
    """The container of a state with specific path cost in a graph."""
    def __init__(self, state):
        self.state = state
        self.name = self.state.name
        self.pathcost = 0
        self.priority = 0
        self.parent = None
        self.removed = False

    def __lt__(self, other):
        return (self.priority) <= (other.priority)

    def setpriority(self):
        self.priority = self.pathcost+self.state.heurcost

    def printself(self):
        print 'pathcost:', self.pathcost
        # print 'heurcost:', self.state.heurcost

    def childnode(self, action):
        newpegs = self.perform_action(action)
        child = Node(State(newpegs))
        child.pathcost = self.pathcost + 1
        child.parent = self
        return child

    def perform_action(self, action):
        newpegs = deepcopy(self.state.pegs)
        peg = newpegs[action[0]]
        newpegs[action[1]].append(peg.pop())
        return newpegs
        

class Heuristic(object):
    """Define heuristic function."""
    def cost(self, state, goal):
        pass

class Admissible(Heuristic):
    """Define admissible heuristic function."""
    def cost(self, state, goal):
        maps = {}
        cost = []
        for i,peg in enumerate(state.pegs):
            for j,disk in enumerate(peg):
                maps[disk] = [(i,j)]
        for i,peg in enumerate(goal.pegs):
            for j,disk in enumerate(peg):
                maps[disk].append((i,j))
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


class NonAdmissible(Admissible):
    """Define admissible heuristic function."""
    def cost(self, state, goal):
        maps = {}
        cost = []
        for i,peg in enumerate(state.pegs):
            for j,disk in enumerate(peg):
                maps[disk] = [(i,j)]
        for i,peg in enumerate(goal.pegs):
            for j,disk in enumerate(peg):
                maps[disk].append((i,j))
        for key,val in maps.iteritems():
            cost.append(self.disktogoal(val[0],val[1],state.pegs))
        return sum(cost)


class Astar(object):
    """A star search algorithm."""
    def setup(self, node, goal, heuristic):
        self.node = node
        self.goal = goal
        self.heuristic = heuristic
        self.node.state.heurcost = self.heuristic.cost(self.node.state, self.goal)
        self.node.setpriority()
        self.frontier = PriorityQueue()
        self.explored = Set()
        self.frontier.add(self.node)

    def actions(self, state):
        actions = []
        for i, peg in enumerate(state.pegs):
            for j in range(len(state.pegs)):
                if (i!=j) and peg:
                    actions.append((i,j))
        return actions

    def search(self, *args):
        while True:
            if self.frontier.isempty():
                print 'There is no any solution.'
                return False
            node = self.frontier.pop()
            if node is None:
                print 'There is no any solution.'
                return False

            if node.state.goaltest(self.goal):
                self.solution = self.backtrack(node)
                self.statistic()
                return True

            self.explored.add(node.name)
            for act in self.actions(node.state):
                child = node.childnode(act)
                child.state.heurcost = self.heuristic.cost(child.state, self.goal)
                child.setpriority()
                if child.name not in self.explored:
                    if not self.frontier.contain(child):
                        self.frontier.add(child)
                    elif self.frontier.getpriority(child) > child.priority:
                        self.frontier.remove(child)
                        self.frontier.add(child)

    def backtrack(self, node):
        sequence  = [node]
        while node.parent is not None:
            sequence.append(node.parent)
            node = node.parent
        return sequence[::-1]

    def statistic(self):
        self.solution_length = self.solution[-1].pathcost 
        self.nodes_expanded = len(self.explored) + self.frontier.getsize()


class RBFS(Astar):
    """Recursive best first search algoritm."""
    def __int__(self):
        self.abc = 0
        self.solution_length = 0

    def search(self, node, flimit):
        if node.state.goaltest(self.goal):
            self.solution = self.backtrack(node)
            self.solution_length = self.solution[-1].pathcost
            return (True, 0)
        children = []
        for act in self.actions(node.state):
            self.abc += 1
            child = node.childnode(act)
            child.state.heurcost = self.heuristic.cost(child.state, self.goal)
            child.setpriority()
            children.append(child)
        if not children:
            return (False, float('inf'))
        for child in children:
            child.priority = max(child.priority, node.priority)

        while True:
            best, alternative = heapq.nsmallest(2, children)
            if best.priority > flimit:
                return (False, best.priority)
            result, best.priority = self.search(best, min(alternative.priority,flimit))
            if result:
                return (result, best.priority)



def test_astar(node, goal):
    heur = Admissible()
    astar = Astar()
    astar.setup(node, goal, heur)
    astar.search()
    print [i.name for i in astar.solution]

def test_rbfs(node, goal):
    heur = Admissible()
    rbfs = RBFS()
    rbfs.setup(node, goal, heur)
    rbfs.search(rbfs.node, float('inf'))
    print [i.name for i in rbfs.solution]

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
    p4 = State([[1,2,3,4,5,6,7,8,9,0],[],[]])
    g4 = State([[6,5,7],[0,3,8,4],[1,9,2]])

    print 'Heuristic Test:'
    test_heuristic(p1,g1)
    test_heuristic(p2,g2)
    test_heuristic(p3,g3)
    test_heuristic(p4,g4)
    print 

    print 'Astar Test:'
    # test_astar(Node(p1),g1)
    # test_astar(Node(p2),g2)
    # test_astar(Node(p3),g3)
    # test_astar(Node(p4),g4)
    print

    print 'RFBS Test:'
    test_rbfs(Node(p1),g1)
    test_rbfs(Node(p2),g2)
    test_rbfs(Node(p3),g3)
    # test_rbfs(Node(p4),g4)
    print














