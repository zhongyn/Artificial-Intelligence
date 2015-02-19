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
        self.backtrack_count = 0
        self.filled_in_number = 0
        self.init_domain()

    def init_domain(self):
        for i in xrange(self.table_size):
            for j in xrange(self.table_size):
                if self.state_table[i][j] == 0:
                    cell = Cell(self.avaible_domain(i,j))
                else:
                    cell = Cell([self.state_table[i][j]])
                    self.filled_in_number += 1
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
        # print 'union:', union
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

    def inference(self, x, y, val, domain_table, *arg):
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
                new_domain_table = self.inference(x,y,val,domain_table,new_state_table)
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

class NakedPairs(Sudoku):
    """Add a naked tripes rule to the inference."""

    def inference(self, x, y, val, domain_table, state_table):
        new_domain_table = deepcopy(domain_table)
        a,b,c,d = self.box_index(x,y)

        unassigned_row = np.where(state_table[x,:]==0)[0]
        unassigned_col = np.where(state_table[:,y]==0)[0]
        unassigned_box = np.where(state_table[a:b,c:d].flat==0)[0]

        for i in unassigned_row:
            if val in new_domain_table[x,i].domain:
                new_domain_table[x,i].remove(val)
        for i in unassigned_col:
            if val in new_domain_table[i,y].domain:
                new_domain_table[i,y].remove(val)
        for i in unassigned_box:
            if val in new_domain_table[a:b,c:d].flat[i].domain:
                new_domain_table[a:b,c:d].flat[i].remove(val)

        self.remove_naked(x,y,unassigned_row,new_domain_table[x,:])
        self.remove_naked(x,y,unassigned_col,new_domain_table[:,y])
        self.remove_naked(x,y,unassigned_box,new_domain_table[a:b,c:d].flat)

        for i in unassigned_row:
            if new_domain_table[x,i].domain_size() == 0:
                return None
        for i in unassigned_col:
            if new_domain_table[i,y].domain_size() == 0:
                return None
        for i in unassigned_box:
            if new_domain_table[a:b,c:d].flat[i].domain_size() == 0:
                return None

        return new_domain_table


    def findintersect(self,unassigned,domain_unit):
        for i in unassigned:
            for j in unassigned:
                if i != j:
                    naked = set(domain_unit[i].domain).union(domain_unit[j].domain)
                    if len(naked) <= 2:
                        return (naked,set([i,j]))
        return None

    def remove_naked(self,x,y,unassigned,domain_unit):
        result = self.findintersect(unassigned, domain_unit)
        if result is not None:
            naked, naked_ids = result
            for i in unassigned:
                if i not in naked_ids:
                    domain_unit[i].domain = list(set(domain_unit[i].domain).difference(naked))


class NakedTriples(NakedPairs):

    def findintersect(self,unassigned,domain_unit):
        for i in unassigned:
            for j in unassigned:
                for k in unassigned:
                    if i != j and i!= k and j!=k:
                        naked = set(domain_unit[i].domain).union(domain_unit[j].domain, domain_unit[k].domain)
                        if len(naked) <= 3:
                            return (naked,set([i,j,k]))
        return None


def readdata_test(filename):
    readdata = ReadData()
    readdata.read_data(filename)
    return readdata.table_list

def sudoku_test(probs):
    result = []
    for i,prob in enumerate(probs):
        sudoku1 = Sudoku(prob, 9)
        sudoku2 = RandomSlot(prob, 9)
        sudoku3 = NakedPairs(prob, 9)
        sudoku4 = NakedTriples(prob, 9)
        sudoku1.backtracking_search()
        sudoku2.backtracking_search()
        sudoku3.backtracking_search()
        sudoku4.backtracking_search()
        tmp = [i+1,sudoku1.backtrack_count,sudoku2.backtrack_count,sudoku3.backtrack_count,sudoku4.backtrack_count,sudoku1.filled_in_number]
        print tmp
        result.append(tmp)
    return result


def naked_test(prob):
    sudoku = NakedTriples(prob, 9)
    sudoku.backtracking_search()
    return sudoku.backtrack_count


if __name__ == '__main__':
    probs = readdata_test('../data/repository.txt')
    for k,v in probs.iteritems():
        print '\n',k
        result = sudoku_test(v)
        average = np.mean(result,axis=0)
        total = np.concatenate((result,[average]),axis=0)
        np.savetxt('../data'+k+'.txt', total, delimiter=',', fmt='%d')





