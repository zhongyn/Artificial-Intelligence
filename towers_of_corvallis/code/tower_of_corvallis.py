from problem_formulation import *

def read_data(filename):
    states = []
    with open(filename) as f:
        f.readline()
        for l in f:
            states.append([int(i) for i in l.rstrip('\n')[::-1]])
    states.pop()
    return [State([i,[],[]]) for i in states]

def output_data(states):
    # return [s.pegs[::-1] for s in states]
    return

class TowerOfCorvallis(object):
    """The game of TowerOfCorvallis."""
    def __init__(self, initstate, algorithm, heuristic):
        self.initstate = initstate
        self.algorithm = algorithm
        self.goal = self.setgoal()
        self.heuristic = heuristic

    def setgoal(self):
        return State([sorted(self.initstate.pegs[0]),[],[]])

    def run(self):
        print self.initstate.name
        print self.goal.name
        self.algorithm.setup(self.initstate, self.goal, self.heuristic)
        self.algorithm.search()
        print 'Finish search'

    def printsolution(self):

        return [[''.join(map(str, i[::-1])) for i in s.pegs] for s in self.algorithm.solution]

def test_toc():
    numdisks = [4]
    states_list = []
    for i in numdisks:
        states_list.append(read_data('../data/perms-'+str(i)+'.txt'))

    heuristics = [Admissible(), NonAdmissible()]

    for heur in heuristics:
        for states in states_list:
            for state in states:
                print
                astar = Astar()
                toc = TowerOfCorvallis(state, astar, heur)
                toc.run()
                print toc.printsolution()



def test_io(filename):
    data = read_data(filename)
    print output_data(data)

if __name__ == '__main__':
    # test_io('../data/perms-4.txt')
    test_toc()