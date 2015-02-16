from sudoku import *

def main(filename):
    readdata = ReadData()
    readdata.read_data(filename)

    for prob in readdata.table_list['Easy']:
        