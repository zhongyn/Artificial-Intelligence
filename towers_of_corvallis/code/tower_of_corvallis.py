from problem_formulation import *
import time
import numpy as np


class TowerOfCorvallis(object):
    """The game of TowerOfCorvallis."""
    def __init__(self, node, algorithm, heuristic):
        self.node = node
        self.algorithm = algorithm
        self.goal = self.setgoal()
        self.heuristic = heuristic
        self.cputime = 0
        self.walltime = 0

    def setgoal(self):
        return State([sorted(self.node.state.pegs[0]),[],[]])

    def run(self):
        self.algorithm.setup(self.node, self.goal, self.heuristic)
        a = time.clock() # cpu time
        b = time.time() # wall time
        self.algorithm.search(self.node, float('inf'))
        self.cputime = time.clock() - a
        self.walltime = time.time() - b
        self.printstatistc()

    def printsolution(self):
        return [[''.join(map(str, i[::-1])) for i in s.state.pegs] for s in self.algorithm.solution]

    def printstatistc(self):
        print 'cputime:', self.cputime
        print 'walltime:', self.walltime
        print 'solution_length:', self.algorithm.solution_length
        print 'nodes_expanded:', self.algorithm.nodes_expanded
        print self.printsolution()
        print 'Finish search\n'

def read_data(filename):
    states = []
    with open(filename) as f:
        f.readline()
        for l in f:
            states.append([int(i) for i in l.rstrip('\n')[::-1]])
    while not states[-1]:
        states.pop()
    return [State([i,[],[]]) for i in states]

def test_astar(numdisks, heuristics):
    states_list = []
    for i in numdisks:
        states_list.append(read_data('../data/perms-'+str(i)+'.txt'))

    per_heur = []
    i = 0
    for heur in heuristics:
        print
        print 'heuristics:', i
        i += 1
        per_size = []
        j = 0
        for states in states_list:
            print 'size of disks:', numdisks[j]
            j += 1
            per_state = []
            k = 0
            print 'number of init states:', len(states)
            # print states
            for state in states:
                k += 1
                # print
                # print k
                # print state.name
                astar = Astar()
                toc = TowerOfCorvallis(Node(state), astar, heur)
                toc.run()
                per_state.append((toc.algorithm.nodes_expanded,toc.algorithm.solution_length,toc.cputime,))

            per_size.append(per_state)
        per_heur.append(per_size)

    astar_result = np.array(per_heur, dtype=[('nodes_expanded',np.uint64),('solution_length',np.uint8),('cputime',np.float)])
    print astar_result
    np.save('../data/astar.npy', astar_result)
    return 


def test_rbfs(numdisks, heuristics):
    states_list = []
    for i in numdisks:
        states_list.append(read_data('../data/perms-'+str(i)+'.txt'))

    per_heur = []
    i = 0
    for heur in heuristics:
        print
        print 'heuristics:', i
        i += 1
        per_size = []
        j = 0
        for states in states_list:
            print 'size of disks:', numdisks[j]
            j += 1
            per_state = []
            k = 0
            print 'number of init states:', len(states)
            # print states
            for state in states:
                k += 1
                # print
                # print k
                # print state.name
                rbfs = RBFS()
                toc = TowerOfCorvallis(Node(state), rbfs, heur)
                toc.run()
                per_state.append((toc.algorithm.nodes_expanded,toc.algorithm.solution_length,toc.cputime,))
            per_size.append(per_state)
        per_heur.append(per_size)

    rbfs_result = np.array(per_heur, dtype=[('nodes_expanded',np.uint64),('solution_length',np.uint8),('cputime',np.float)])
    print rbfs_result
    np.save('../data/rbfs.npy', rbfs_result)
    return 

def main():
    heuristics = [Admissible(), NonAdmissible()]
    # test_astar([9], heuristics)
    test_rbfs([4,5], heuristics)


if __name__ == '__main__':
    main()




