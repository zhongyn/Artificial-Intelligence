# import problem_formulation as pf

def read_data(filename):
    states = []
    with open(filename) as f:
        f.readline()
        for l in f:
            states.append([int(i) for i in l.rstrip('\n')[::-1]])
    states.pop()
    return states

def output_data(states):
    return [i[::-1] for i in states]


class TowerOfCorvallis(object):
    """The game of TowerOfCorvallis."""
    def __init__(self, input, algorithm, goal):
        # self.algorithm = algorithm
        pass



def test_io(filename):
    data = read_data(filename)
    print data
    print output_data(data)

if __name__ == '__main__':
    test_io('../data/perms-4.txt')