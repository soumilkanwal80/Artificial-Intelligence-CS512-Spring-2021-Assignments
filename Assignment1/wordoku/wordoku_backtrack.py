import string, math, copy, numpy as np
import time
import enchant

class Wordoku:
    def __init__(self, path, out_path):
        self.chars = []
        self.path = path
        self.out_path = out_path
        self.wordoku = []
        self.wordoku_dim = -1
        self.backtrack_count = -1
        self.state = []
        self.__readFile(path)
        self.__initState()

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
                    temp.append('')
            self.state.append(temp)
        
        for i in range(self.wordoku_dim):
            for j in range(self.wordoku_dim):
                if self.wordoku[i][j] != '*':
                    self.state = self.propagate_constraints(self.state, i, j, self.wordoku[i][j])



    def check_used_row(self, row_num, char):
        for i in range(self.wordoku_dim):
            if self.wordoku[row_num][i] == char:
                return False
        return True

    def check_used_column(self, col_num, char):
        for i in range(self.wordoku_dim):
            if self.wordoku[i][col_num] == char:
                return False
        return True

    def check_used_box(self, row_num, col_num, char):
        temp = int(math.sqrt(self.wordoku_dim))
        for i in range(temp):
            for j in range(temp):
                if self.wordoku[row_num - row_num%temp + i][col_num - col_num%temp + j] == char:
                    return False
        return True

    def find_next_empty2(self):
        for i in range(self.wordoku_dim):
            for j in range(self.wordoku_dim):
                if self.wordoku[i][j] == '*':
                    return i, j

        return False, False

    def find_next_empty(self, state):
        min_idx = (0, 0)
        min_const = 100
        isFull = False
        for i in range(self.wordoku_dim):
            for j in range(self.wordoku_dim):
                if self.wordoku[i][j]=='*':
                    if len(state[i][j])<min_const:
                        min_idx = (i, j)
                        min_const = len(state[i][j])
                        isFull = True
        if isFull == True:
            return min_idx[0], min_idx[1]
        else:
            return -1, -1

    def num_constraints_row(self, state, row_num, char):
        count = 0
        for i in range(self.wordoku_dim):
            if char in state[row_num][i]:
                count+=1
        return count 
    def num_constraints_col(self, state, col_num, char):
        count = 0
        for i in range(self.wordoku_dim):
            if char in state[i][col_num]:
                count+=1
        return count 
    
    def num_constraints_box(self, state, row_num, col_num, char):
        temp = int(math.sqrt(self.wordoku_dim))
        count = 0
        for i in range(temp):
            for j in range(temp):
                if char in state[row_num - row_num%temp + i][col_num - col_num%temp + j]:
                    count+=1
        return count


    def find_min_constrained_value(self, state, row_idx, col_idx):
        possible_chars = state[row_idx][col_idx]
        char_to_return = []
        char_constraint_val = []
        for char in possible_chars:
            total_constraint = self.num_constraints_row(state, row_idx, char) + self.num_constraints_col(state, col_idx, char) + self.num_constraints_box(state, row_idx, col_idx, char)
            char_constraint_val.append(total_constraint)
            char_to_return.append(char)
        idx = np.argsort(np.array(char_constraint_val))
        char_to_return2 = []
        for i in range(idx.shape[0]):
            char_to_return2.append(char_to_return[idx[i]])
        return char_to_return2

    def check_safe_location(self, row_idx, col_idx, char):
        return self.check_used_row(row_idx, char) and self.check_used_column(col_idx, char) and self.check_used_box(row_idx, col_idx, char)
    

    def propagate_constraints(self, state, row_idx, col_idx, char):
        self.backtrack_count +=1
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
            state[i][j] = state[i][j].replace(char, '')
        return state

    def solveHelper(self, state):
        row, col = self.find_next_empty(state)
        if row == -1 and col == -1:
            return True
        chars = self.find_min_constrained_value(state, row, col)

        for char in chars:

            self.wordoku[row][col] = char
            new_state = self.propagate_constraints(copy.deepcopy(state), row, col, char)

            if self.solveHelper(copy.deepcopy(new_state)) == True:
                return True
            self.wordoku[row][col] = '*'
        
        return False

    def solve(self):
        self.solveHelper(copy.deepcopy(self.state))
    
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
            print('Number of Nodes: ', self.backtrack_count)
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
    # path= './test_cases/input5.txt'
    path = input("Enter Input File path: ")
    # out_path = './output/output5.txt'
    out_path = input("Enter Output File path: ")
    wordoku  = Wordoku(path, out_path)
    start2 = time.time()
    wordoku.solve()
    end2 = time.time() - start2
    wordoku.print()
    wordoku.findMeaning()
    end1 = time.time() - start1
    print('Total Time: ', end1)
    print('Search Time: ', end2)

