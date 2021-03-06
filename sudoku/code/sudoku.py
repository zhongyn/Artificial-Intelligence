import numpy as np
from copy import deepcopy
import random as rd

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
        self.table_list = {k:np.array(v) for k,v in self.table_list.iteritems()}

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

    #-------------------
    #Init tables
    #-------------------
    def __init__(self, table, size):
        self.state_table = table
        self.table_size = size
        self.basic_domain = np.arange(1,size+1)
        self.domain_table = np.empty([size,size], dtype=object)
        self.domain_size_table = np.empty([size,size], dtype=int)
        self.init_domain()
        self.backtrack_count = 0

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

    #-------------------------
    #Backtracking search
    #-------------------------
    def neighbor_domain_union(self, x, y, domain_table):
        a,b,c,d = self.box_index(x,y)
        union = set()
        for i in domain_table[x,:]:
            union.update(i.domain)
        for i in domain_table[:,y]:
            union.update(i.domain)
        for i in domain_table[a:b,c:d].flat:
            union.update(i.domain)
        return union

    def select_unassigned_variable(self, state_table, domain_size_table):
        # selects the most constrained cell.
        unassigned = np.where(state_table==0)
        mrv_variable = np.argmin(domain_size_table[unassigned])
        return (unassigned[0][mrv_variable], unassigned[1][mrv_variable])

    def order_domain_variable(self, x, y, domain_table):
        domain = domain_table[x][y].domain
        if domain_table[x][y].domain_size() == 1:
            return domain
        union = self.neighbor_domain_union(x,y,domain_table)
        lsv = []
        normal = []
        for val in domain:
            if val not in union:
                lsv.append(val)
            else:
                normal.append(val)
        return lsv+normal

    def inference(self, x, y, val, domain_table):
        new_domain_table = deepcopy(domain_table)
        new_domain_table[x][y].domain.extend([val]*3)
        a,b,c,d = self.box_index(x,y)
        for i in new_domain_table[x,:]:
            if val in i.domain:
                i.remove(val)
                if i.domain_size() == 0:
                    return None
        for i in new_domain_table[:,y]:
            if val in i.domain:
                i.remove(val)
                if i.domain_size() == 0:
                    return None
        for i in new_domain_table[a:b,c:d].flat:
            if val in i.domain:
                i.remove(val)
                if i.domain_size() == 0:
                    return None
        new_domain_table[x][y].domain = [val]
        return new_domain_table

    def update_domain_size(self, domain_table):
        domain_size_table = np.empty([self.table_size,self.table_size], dtype=int)
        for i in xrange(self.table_size):
            for j in xrange(self.table_size):
                domain_size_table[i][j] = domain_table[i][j].domain_size()
        return domain_size_table

    def incomplete(self, state_table):
        if np.where(state_table==0)[0].size:
            return True
        return False

    def consistent(self, x, y, val, state_table):
        a,b,c,d = self.box_index(x,y)
        if val in state_table[x,:]:
            return False
        if val in state_table[:,y]:
            return False
        if val in state_table[a:b,c:d]:
            return False
        return True

    def backtrack(self, state_table, domain_table, domain_size_table):
        if not self.incomplete(state_table):
            return state_table
        x,y = self.select_unassigned_variable(state_table, domain_size_table)
        order_var = self.order_domain_variable(x,y,domain_table)
        # print order_var
        for val in order_var:
            if self.consistent(x,y,val,state_table):
                new_state_table = state_table.copy()
                new_state_table[x][y] = val
                new_domain_table = self.inference(x,y,val,domain_table)
                if new_domain_table is not None:
                    new_domain_size_table = self.update_domain_size(new_domain_table)
                    result = self.backtrack(new_state_table, new_domain_table, new_domain_size_table)
                    if result is not None:
                        return result
        self.backtrack_count += 1
        return None

    def backtracking_search(self):
        self.backtrack(self.state_table, self.domain_table, self.domain_size_table)

class RandomSlot(Sudoku):
    """Instead of picking the most constrained slot, pick a slot randomly."""

    def select_unassigned_variable(self, state_table, *arg):
        unassigned = np.where(state_table==0)
        # rand_id = rd.randrange(unassigned[0].size)
        rand_id = 0
        return (unassigned[0][rand_id], unassigned[1][rand_id])

# class NakedTriples(Sudoku):
#     """Add a naked tripes rule to the inference."""

#     def inference(self, x, y, val, domain_table, k=2, state_table):
#         new_domain_table = deepcopy(domain_table)
#         new_domain_table[x][y].domain.extend([val]*3)
#         a,b,c,d = self.box_index(x,y)
#         unassigned_row = np.where(state_table[x,:]==0)
#         unassigned_col = np.where(state_table[:,y]==0)
#         unassigned_box = np.where(state_table[a:b,c:d].flat==0)

#         triple, triple_ids = self.findintersect(unassigned_row)
#         unassigned_size = unassigned_row[0].size
#         while tmp is not None:
#             for i in unassigned_row:
#                 if i not in triple_ids:
#                     domain_table[x][i].domain

#         for i in new_domain_table[x,:]:
#             if val in i.domain:
#                 i.remove(val)
#                 if i.domain_size() == 0:
#                     return None
#         for i in new_domain_table[:,y]:
#             if val in i.domain:
#                 i.remove(val)
#                 if i.domain_size() == 0:
#                     return None
#         for i in new_domain_table[a:b,c:d].flat:
#             if val in i.domain:
#                 i.remove(val)
#                 if i.domain_size() == 0:
#                     return None
#         new_domain_table[x][y].domain = [val]
#         return new_domain_table





def readdata_test(filename):
    readdata = ReadData()
    readdata.read_data(filename)
    return readdata.table_list

def sudoku_test(prob):
    print 'count:',sudoku.backtrack_count

def sudoku_random_test(pr):
    result = []
    for i, prob in enumerate(pr):
        print '\nproblem:',i
        sudoku1 = Sudoku(prob, 9)
        sudoku1.backtracking_search()
        sudoku2 = RandomSlot(prob, 9)
        sudoku2.backtracking_search()
        result.append([i+1, sudoku1.backtrack_count, sudoku2.backtrack_count])
    return result




if __name__ == '__main__':
    probs = readdata_test('../data/repository.txt')
    for k,v in probs.iteritems():
        np.savetxt('../data/'+k+'.txt, sudoku_random_test(v), delimiter=',', fmt='%d')








