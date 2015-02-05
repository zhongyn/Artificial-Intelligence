from problem_formulation import *
import time

def read_data(filename):
    states = []
    with open(filename) as f:
        f.readline()
        for l in f:
            states.append([int(i) for i in l.rstrip('\n')[::-1]])
    states.pop()
    return [State([i,[],[]]) for i in states]


class TowerOfCorvallis(object):
    """The game of TowerOfCorvallis."""
    def __init__(self, node, algorithm, heuristic):
        self.node = node
        self.algorithm = algorithm
        self.goal = self.setgoal()
        self.heuristic = heuristic
        self.cputime = 0

    def setgoal(self):
        return State([sorted(self.node.state.pegs[0]),[],[]])

    def run(self):
        self.algorithm.setup(self.node, self.goal, self.heuristic)
        a = time.clock()
        self.algorithm.search(self.node, float('inf'))
        self.cputime = time.clock() - a
        print 'time:', self.cputime
        print 'solution_length:', self.algorithm.solution_length
        print 'nodes_expanded:', self.algorithm.nodes_expanded
        print 'Finish search'

    def printsolution(self):
        return [[''.join(map(str, i[::-1])) for i in s.state.pegs] for s in self.algorithm.solution]


def test_toc():
    numdisks = [4]
    states_list = []
    for i in numdisks:
        states_list.append(read_data('../data/perms-'+str(i)+'.txt'))

    heuristics = [Admissible(), NonAdmissible()]

    for heur in heuristics:
        for states in states_list:
            i = 0
            for state in states:
                i += 1
                print
                print 'state:', i
                print state.name
                astar = Astar()
                toc = TowerOfCorvallis(Node(state), astar, heur)
                toc.run()

    for heur in heuristics:
        for states in states_list:
            i = 0
            for state in states:
                i += 1
                print
                print 'state:', i
                print state.name
                rbfs = RBFS()
                toc = TowerOfCorvallis(Node(state), rbfs, heur)
                toc.run()


def test_io(filename):
    data = read_data(filename)
    print output_data(data)

if __name__ == '__main__':
    # test_io('../data/perms-4.txt')
    test_toc()




