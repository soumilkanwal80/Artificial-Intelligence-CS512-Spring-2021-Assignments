import string, math, copy, numpy as np
from tqdm import tqdm
from random import randint, seed
import time, enchant
seed(0)
count = 0
class Wordoku:
    def __init__(self, path, out_path):
        self.chars = []
        self.wordoku = []
        self.wordoku_dim = -1
        self.state = []
        self.out_path = out_path
        self.__readFile(path)
        self.__initState()
        self.__initWordoku()

        self.max_steps = int(1e9)


    def __readFile(self, path):
        worduk_file = open(path, 'r')
        Lines = worduk_file.readlines()
        possible_chars = set()
        for line in Lines:
            x = list(line)
            if x[-1] == '\n':
                x = x[:-1]
            self.wordoku.append(x)
            for i in x:
                if i!='*':
                    possible_chars.add(i)
                
        self.wordoku_dim = len(self.wordoku)
        self.chars = list(possible_chars)

    def __initState(self):
        x = ''.join(self.chars)
        for i in range(self.wordoku_dim):
            temp = []
            for j in range(self.wordoku_dim):
                if self.wordoku[i][j] == '*':
                    temp.append(x)
                else:
                    temp.append('0')
            self.state.append(temp)
        
        for i in range(self.wordoku_dim):
            for j in range(self.wordoku_dim):
                if self.state[i][j] == '0':
                    self.refine_constraints(i, j, self.wordoku[i][j])

    def __initWordoku(self):
        for i in range(self.wordoku_dim):
            for j in range(self.wordoku_dim):
                if self.state[i][j] != '0':
                    idx = randint(0, len(self.state[i][j])-1)
                    self.wordoku[i][j] = self.state[i][j][idx]
    
    def refine_constraints(self, row_idx, col_idx, char):
        locations = set()
        for i in range(self.wordoku_dim):
             locations.add(row_idx*self.wordoku_dim + i)
             locations.add(i*self.wordoku_dim + col_idx)

        temp = int(math.sqrt(self.wordoku_dim))
        for i in range(temp):
            for j in range(temp):
                r = row_idx - row_idx%temp + i
                c = col_idx - col_idx%temp + j
                locations.add(r*self.wordoku_dim + c)
        
        locations = list(locations)
        for location in locations:
            i = location//self.wordoku_dim
            j = location%self.wordoku_dim
            self.state[i][j] = self.state[i][j].replace(char, '')


    def num_constraints_row(self, row_num, char):
        count = 0
        for i in range(self.wordoku_dim):
            if char in self.wordoku[row_num][i]:
                count+=1
        return count -1

    def num_constraints_col(self, col_num, char):
        count = 0
        for i in range(self.wordoku_dim):
            if char in self.wordoku[i][col_num]:
                count+=1
        return count -1
    
    def num_constraints_box(self, row_num, col_num, char):
        temp = int(math.sqrt(self.wordoku_dim))
        count = 0
        for i in range(temp):
            for j in range(temp):
                if char in self.wordoku[row_num - row_num%temp + i][col_num - col_num%temp + j]:
                    count+=1
        return count-1

    def getTotalConstraintCell(self, row_num, col_num, char):
        return self.num_constraints_row(row_num, char) + self.num_constraints_col(col_num, char) + self.num_constraints_box(row_num, col_num, char)     


    def find_next_empty(self, epochs = 1000):
        constrained_vars = []
        for i in range(self.wordoku_dim):
            for j in range(self.wordoku_dim):
                if self.state[i][j]!='0':
                    #tc = self.num_constraints_row(i, self.wordoku[i][j]) + self.num_constraints_col(j, self.wordoku[i][j]) + self.num_constraints_box(i, j, self.wordoku[i][j])
                    tc = self.getTotalConstraintCell(i, j, self.wordoku[i][j])
                    if tc != 0:
                        constrained_vars.append([i, j])
        if constrained_vars==[]:
            return -1, -1
        else:    
            pos = randint(0, len(constrained_vars)-1)
            return constrained_vars[pos][0], constrained_vars[pos][1]


    
    def minimizeConflict(self, row_num, col_num):
        curr_char = self.wordoku[row_num][col_num]
        # curr_tc = self.num_constraints_row(row_num, curr_char) + self.num_constraints_col(col_num, curr_char) + self.num_constraints_box(row_num, col_num, curr_char) 
        curr_tc = 1000
        possible_ = copy.deepcopy(self.state[row_num][col_num]).replace(curr_char, '')
        
        for char in possible_:
            self.wordoku[row_num][col_num] = char
            tc = self.getTotalConstraintCell(row_num, col_num, char)
            if tc<curr_tc:
                curr_tc = tc
                curr_char= char
        self.wordoku[row_num][col_num] = curr_char
        return curr_char

    def solveHelper(self):
        global count
        count+=1
        row, col = self.find_next_empty()
        if row == -1 and col == - 1:
            return True
        x = self.minimizeConflict(row, col)



    def findTotalConflict(self):
        cnf = 0
        for i in range(self.wordoku_dim):
            for j in range(self.wordoku_dim):
                if self.state[i][j]!='0':
                    cnf+=self.getTotalConstraintCell(i, j, self.wordoku[i][j])
        return cnf

    def solve(self):
        for i in range(500):
            self.solveHelper()
            if self.verify() == True:
                return True
        # print(self.findTotalConflict())
            # self.print()
            # print('\n')

    
    def print(self):
        for i in range(self.wordoku_dim):
            for j in range(self.wordoku_dim):
                print(self.wordoku[i][j], end = " ")
            print()

        file = open(self.out_path, 'w')
        for i in self.wordoku:
            file.write(''.join(i))
            file.write('\n')

        if self.verify() == True:
            print("Correct Solution")
        else:
            print("Incorrect Solution")

    def findMeaning(self):
        d = enchant.Dict("en_US")
        print("Valid Words")
        
        for i in range(self.wordoku_dim):
            row_list = []
            col_list = []
            for j in range(self.wordoku_dim):
                row_list.append(self.wordoku[i][j])
                col_list.append(self.wordoku[j][i])
            if d.check(''.join(row_list)):
                print(''.join(row_list))
            if d.check(''.join(col_list)):
                print(''.join(col_list))
        diag_list = []
        for i in range(self.wordoku_dim):
            diag_list.append(self.wordoku[i][i])
        if d.check(''.join(diag_list)):
            print(''.join(diag_list))


    def verify(self):
        for i in range(self.wordoku_dim):
            row_set = set()
            col_set = set()
            for j in range(self.wordoku_dim):
                row_set.add(self.wordoku[i][j])
                col_set.add(self.wordoku[j][i])
            if(len(list(row_set)) != self.wordoku_dim):
                return False
            if(len(list(col_set)) != self.wordoku_dim):
                return False
        temp = int(math.sqrt(self.wordoku_dim))
        for i in range(int(self.wordoku_dim//temp)):
            for j in range(int(self.wordoku_dim//temp)):
                box_set = set()
                for i1 in range(temp):
                    for j1 in range(temp):
                        box_set.add(self.wordoku[i*temp + i1][j*temp + j1])
                if(len(list(box_set))!=self.wordoku_dim):
                    return False
        return True

if __name__ == "__main__":
    start1 = time.time()
    path= './test_cases/input5.txt'
    # path = input("Enter Input File path: ")
    out_path = './output/output5.txt'
    # out_path = input("Enter Output File path: ")
    start2 = time.time()
    for i in tqdm(range(int(1000000))):
        wordoku  = Wordoku(path, out_path)
        if wordoku.solve() == True:
            break
    end2 = time.time()
    print('Search Time: ', end2 - start2)
    wordoku.print()
    wordoku.findMeaning()
    print('Number of Nodes: ', count)
    end1 = time.time()
    print('Total Time: ', end1 - start1)
