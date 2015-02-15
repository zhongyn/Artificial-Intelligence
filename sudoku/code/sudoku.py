import numpy as np

class ReadData(object):
    """Import data as sudoku tables."""
    def __init__(self):
        self.catalog = ['Easy', 'Medium', 'Hard', 'Evil']
        self.table_list = {}

    def read_data(self, filename):
        for i in self.catalog:
            self.table_list[i] = []
        with open(filename) as f:
            for line in f:
                if line == '\n':
                    continue
                if self.is_title(line):
                    cata = self.get_catatog(line)
                    table = []
                    for i in xrange(9):
                        table.append(self.string_to_int(f.next()))
                    self.table_list[cata].append(table)

    def is_title(self, line):
        a,b = line.split()
        if b in self.catalog:
            return True
        return False

    def get_catatog(self, line):
        a,b = line.split()
        return b

    def string_to_int(self, line):
        row = []
        for i in line.split():
            for j in i:
                row.append(int(j))
        return row

def readdata_test(filename):
    readdata = ReadData()
    readdata.read_data(filename)

    for k,v in readdata.table_list.items():
        print k,
        print v

class Cell(object):
    """Represents a cell in the sudoku table."""

    def __init__(self, domain):
        self.domain = domain

    def remove(self, val):
        self.domain.remove(val)

    def domain_size(self):
        return len(self.domain)



class Sudoku(object):
    """A sudoku solver implmented with backtracking search."""

    def __init__(self, table, size):
        self.state_table = table
        self.table_size = size
        self.basic_domain = np.arange(1,size+1)
        self.domain_table = np.empty([size,size], dtype=object)
        self.domain_size_table = np.empty([size,size], dtype=int)
        self.init_domain()

    def init_domain(self):
        for i in xrange(self.table_size):
            for j in xrange(self.table_size):
                if self.state_table[i][j] == 0:
                    cell = Cell(self.avaible_domain(i,j))
                else:
                    cell = Cell([self.state_table[i][j]])
                self.domain_table[i][j] = cell
                self.domain_size_table[i][j] = cell.domain_size()     

    def avaible_domain(self, i, j):
        a,b,c,d = self.box_index(i,j)
        tmp = np.setdiff1d(self.basic_domain, self.state_table[i,:])
        tmp = np.setdiff1d(tmp, self.state_table[:,j])
        tmp = np.setdiff1d(tmp, self.state_table[a:b,c:d])
        return tmp.tolist()

    def box_index(self, x, y):
        return ((x/3)*3, (x/3+1)*3, (y/3)*3, (y/3+1)*3)

    def select_unassigned_variable(self, state_table, domain_size_table):
        # selects the most constrained cell.
        unassigned = np.where(state_table==0)
        mrv_variable = np.argmin(domain_size_table[unassigned])
        return (unassigned[0][mrv_variable], unassigned[1][mrv_variable])

    def order_domain_variable(self, x, y, domain_table, domain_size_table):
        domain = domain_table[x][y].domain
        if domain_size_table[x][y] == 1:
            return domain[0]


    def neighbor_union(self, x, y, val):
        a,b,c,d = self.box_index(x,y)
        for cell in np.nditer(domain_table[x,:]):
            if val in cell.domain:
                return False
        for cell in np.nditer(domain_table[:,y]):
            if val in cell.domain:
                return False
        for cell in np.nditer(domain_table[a:b,c:d]):
            if val in cell.domain:
                return False
        return True



    def inference():
        pass

    def backtrack(self, assignment, ):
        if assignment:
            return assignment
        vx,vy = self.select  

    def run_backtracking_search():
        pass



# class DomainTable(object):
#     """A table of domains."""

#     def __init__(self, domaintable):
#         self.domaintable = domaintable

#     def deltete_domain(self):
#         pass

#     def inference(self):
#         pass




if __name__ == '__main__':
    readdata_test('../data/repository.txt')


