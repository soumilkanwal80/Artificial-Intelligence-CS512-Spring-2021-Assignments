import numpy as np
from random import randint, seed, choice
from tqdm import tqdm
import copy
seed(1)

blocked_square = (4, 3)
xavier_school = (5, 5)
grid_dim = 5
jean_positions = [(5, 2), (1, 5)]
moves_list = [(1, 0), (0, 1), (0, -1), (-1, 0)]

def bfs(magneto_pos, wolverinePos):
    starting_pos = magneto_pos
    ending_pos = wolverinePos

    visited = np.zeros((grid_dim, grid_dim), dtype=np.uint8)
    visited[blocked_square[0] - 1][blocked_square[1] - 1] = 1   
    visited[starting_pos[0] -1][starting_pos[1] - 1] = 1     
    q = []
    q.append([starting_pos[0], starting_pos[1], 0])
    while(len(q)>0):
        front = q[0]
        q.pop(0)
        if((front[0], front[1]) == ending_pos):
            return front[2]
        
        for move in moves_list:
            temp = (front[0] + move[0], front[1] + move[1])
            if temp[0]< grid_dim+1 and temp[0]> 0 and temp[1] < grid_dim+1 and temp[1]> 0 and visited[temp[0]-1][temp[1]-1]== 0:
                q.append([temp[0], temp[1], front[2] + 1])
                visited[temp[0]-1][temp[1]-1] = 1

def checkValidMoveMagneto(next_pos):
    if next_pos[0]< grid_dim+1 and next_pos[0]> 0 and next_pos[1] < grid_dim+1 and next_pos[1]> 0:
        if next_pos != xavier_school and next_pos != blocked_square:
            return True
    return False

def nextMagnetoMove(magnetoPosition, wolverinePosition):
    starting_pos = magnetoPosition
    list_dist = []
    for move in moves_list:
        if checkValidMoveMagneto((starting_pos[0] + move[0], starting_pos[1] + move[1])) == True:
            dist = bfs((starting_pos[0] + move[0], starting_pos[1] + move[1]), wolverinePosition)
            list_dist.append(dist)
        else:
            list_dist.append(1000)
    min_dist = min(list_dist)
    indices = [i for i in range(len(list_dist)) if list_dist[i] == min_dist]
    next_moves_list = [moves_list[i] for i in indices]
    return next_moves_list

class Jean(object):
    def __init__(self):
        self.possible_position = [(5, 2), (1, 5)]
        self.pos_bool = randint(0, 1)
    
    def getCurrentPosition(self):
        return self.possible_position[self.pos_bool]

    def nextMove(self):
        if randint(1, 10) >= 9:
            self.pos_bool = 1- self.pos_bool
        
        return self.getCurrentPosition()




class ActiveMagneto(object):
    def __init__(self):
        self.pos = (randint(1, 5), randint(1, 5))
        while True:
            if self.checkValidMove(self.pos) == False:
                self.pos = (randint(1, 5), randint(1, 5))
            else:
                break
        self.possible_moves = [(1, 0), (0, 1), (0, -1), (-1, 0)]
    def checkValidMove(self, next_pos):
        if next_pos[0]< grid_dim+1 and next_pos[0]> 0 and next_pos[1] < grid_dim+1 and next_pos[1]> 0:
            if next_pos != xavier_school and next_pos != blocked_square:
                return True
        return False

    def getCurrentPosition(self):
        return self.pos

    def bfs(self, magneto_pos, wolverinePos):
        starting_pos = magneto_pos
        ending_pos = wolverinePos

        visited = np.zeros((grid_dim, grid_dim), dtype=np.uint8)
        # visited[xavier_school[0] - 1][xavier_school[1] -1] = 1
        visited[blocked_square[0] - 1][blocked_square[1] - 1] = 1   
        visited[starting_pos[0] -1][starting_pos[1] - 1] = 1     
        q = []
        q.append([starting_pos[0], starting_pos[1], 0])
        while(len(q)>0):
            front = q[0]
            q.pop(0)
            if((front[0], front[1]) == ending_pos):
                return front[2]
            
            for move in moves_list:
                temp = (front[0] + move[0], front[1] + move[1])
                if temp[0]< grid_dim+1 and temp[0]> 0 and temp[1] < grid_dim+1 and temp[1]> 0 and visited[temp[0]-1][temp[1]-1]== 0:
                    q.append([temp[0], temp[1], front[2] + 1])
                    visited[temp[0]-1][temp[1]-1] = 1



    def nextMove(self, wolverinePosition):
        starting_pos = self.pos
        list_dist = []
        for move in moves_list:
            if self.checkValidMove((starting_pos[0] + move[0], starting_pos[1] + move[1])) == True:
                dist = self.bfs((starting_pos[0] + move[0], starting_pos[1] + move[1]), wolverinePosition)
                list_dist.append(dist)
            else:
                list_dist.append(1000)
        min_dist = min(list_dist)
        indices = [i for i in range(len(list_dist)) if list_dist[i] == min_dist]

        rand_index = choice(indices)
        next_move = moves_list[rand_index]
        if randint(1, 20)<=19:
            self.pos= (next_move[0] + self.pos[0], next_move[1] + self.pos[1])

        return self.pos

def checkValidMoveWolverine(next_pos):
    if next_pos[0]< grid_dim+1 and next_pos[0]> 0 and next_pos[1] < grid_dim+1 and next_pos[1]> 0:
        if next_pos != blocked_square:
            return True
    return False

class MDP:
    def __init__(self):
        self.states = {}
        self.policy = {}
        self.isEndState = {}
        self.discount = 0.85
        self.movementProb = 0.95
        self.jeanMovementProb = 0.2
        self.converge_eps = 1e-1
        
        for magneto_i in range(1, grid_dim+1):
            for magneto_j in range(1, grid_dim+1):
                if (magneto_i, magneto_j) == xavier_school or (magneto_i, magneto_j) == blocked_square:
                    continue
                for wolverine_i in range(1, grid_dim+1):        
                    for wolverine_j in range(1, grid_dim+1):
                        if (wolverine_i, wolverine_j) == blocked_square:
                            continue

                        for jean_pos in jean_positions:
                            if (wolverine_i, wolverine_j) == jean_pos and (magneto_i!=wolverine_i or magneto_j != wolverine_j):
                                self.states[(magneto_i, magneto_j, wolverine_i, wolverine_j, ) + jean_pos] = 20
                                self.isEndState[(magneto_i, magneto_j, wolverine_i, wolverine_j, ) + jean_pos] = 1
                            elif (wolverine_i, wolverine_j) == jean_pos and magneto_i == wolverine_i and magneto_j == wolverine_j:
                                self.states[(magneto_i, magneto_j, wolverine_i, wolverine_j, ) + jean_pos] = -15
                                self.isEndState[(magneto_i, magneto_j, wolverine_i, wolverine_j, ) + jean_pos] = 1
                            elif (wolverine_i, wolverine_j) != jean_pos and magneto_i == wolverine_i and magneto_j == wolverine_j:
                                self.states[(magneto_i, magneto_j, wolverine_i, wolverine_j, ) + jean_pos] = -20
                                self.isEndState[(magneto_i, magneto_j, wolverine_i, wolverine_j, ) + jean_pos] = 1
                            else:
                                self.states[(magneto_i, magneto_j, wolverine_i, wolverine_j, ) + jean_pos] = 0
                                self.isEndState[(magneto_i, magneto_j, wolverine_i, wolverine_j, ) + jean_pos] = 0

    def checkValidMoveWolverine(self, next_pos):
        if next_pos[0]< grid_dim+1 and next_pos[0]> 0 and next_pos[1] < grid_dim+1 and next_pos[1]> 0:
            if next_pos != blocked_square:
                return True
        return False
    def checkValidMoveMagneto(self, next_pos):
        if next_pos[0]< grid_dim+1 and next_pos[0]> 0 and next_pos[1] < grid_dim+1 and next_pos[1]> 0:
            if next_pos != blocked_square and next_pos!= xavier_school:
                return True
        return False
    
    def train(self):
        states_temp = {}
        
        max_iterations = int(1e5)
        
        print("Training......")
        for _ in tqdm(range(max_iterations)):
            converged = True
            for key in self.states.keys():
                if self.isEndState[key] == 1:
                    states_temp[key] = self.states[key]
                    self.policy[key] = None
                    continue
                possible_s = []
                possible_act = []
                # for each possible action that wolverine can take
                for action in moves_list:
                    # current position of all three characters
                    magneto_pos = (key[0], key[1])
                    wolverine_pos = (key[2], key[3])
                    jean_pos = (key[4], key[5])
                    # get the next wolverine position and check if its valid(staying inside grid, etc)
                    next_wolverine_pos = tuple(map(lambda i, j: i + j, wolverine_pos, action))
                    if self.checkValidMoveWolverine(next_wolverine_pos) == True:
                        # explore all possible states for this wolverine move
                        q_sa = 0
                        
                        #count all possible moves of magneto????????
                        magneto_moves_list = nextMagnetoMove(magneto_pos, next_wolverine_pos)
                        count_valid_mag_moves = len(magneto_moves_list)
                        # for mag_action in moves_list:
                        #     next_magneto_pos = tuple(map(lambda i, j: i + j, magneto_pos, mag_action))
                        #     if self.checkValidMoveMagneto(next_magneto_pos) == True:
                        #         count_valid_mag_moves+=1
                        
                        # for each possible move of jean and magneto find the transition function, v(s'), reward
                        for mag_action in magneto_moves_list:
                            transition_prob = self.movementProb*self.movementProb/count_valid_mag_moves
                            for jean_action in jean_positions:
                                next_magneto_pos = tuple(map(lambda i, j: i + j, magneto_pos, mag_action))
                                if self.checkValidMoveMagneto(next_magneto_pos):
                                    if jean_pos == jean_action:
                                        transition_prob*=(1-self.jeanMovementProb)
                                        next_state = next_magneto_pos + next_wolverine_pos + jean_pos
                                    else:
                                        transition_prob*=self.jeanMovementProb
                                        next_state = next_magneto_pos + next_wolverine_pos + jean_action
                                    

                                    if self.isEndState[next_state] == True:
                                        q_sa  += transition_prob*(self.states[next_state] + 0)
                                    else:
                                        q_sa += transition_prob*(0 + self.states[next_state]*self.discount)


                        # when magneto doesnt move with prob 0.05
                        transition_prob = self.movementProb*(1-self.movementProb)
                        for jean_action in jean_positions:
                            next_magneto_pos = magneto_pos

                            if jean_pos == jean_action:
                                transition_prob*=(1-self.jeanMovementProb)
                                next_state = next_magneto_pos + next_wolverine_pos + jean_pos
                            else:
                                transition_prob*=self.jeanMovementProb
                                next_state = next_magneto_pos + next_wolverine_pos + jean_action
                            

                            if self.isEndState[next_state] == True:
                                q_sa += transition_prob*(self.states[next_state] + 0)
                            else:
                                q_sa += transition_prob*(0 + self.states[next_state]*self.discount)

                        #When wolverine doesnt move
                        magneto_moves_list = nextMagnetoMove(magneto_pos, wolverine_pos)
                        count_valid_mag_moves = len(magneto_moves_list)
                        for mag_action in magneto_moves_list:
                            transition_prob = (1-self.movementProb)*self.movementProb/count_valid_mag_moves
                            for jean_action in jean_positions:
                                next_magneto_pos = tuple(map(lambda i, j: i + j, magneto_pos, mag_action))
                                if self.checkValidMoveMagneto(next_magneto_pos):
                                    if jean_pos == jean_action:
                                        transition_prob*=(1-self.jeanMovementProb)
                                        next_state = next_magneto_pos + wolverine_pos + jean_pos
                                    else:
                                        transition_prob*=self.jeanMovementProb
                                        next_state = next_magneto_pos + wolverine_pos + jean_action
                                    

                                    if self.isEndState[next_state] == True:
                                        q_sa  += transition_prob*(self.states[next_state] + 0)
                                    else:
                                        q_sa += transition_prob*(0 + self.states[next_state]*self.discount)


                        # when magneto doesnt move with prob 0.05
                        transition_prob = (1-self.movementProb)*(1-self.movementProb)
                        for jean_action in jean_positions:
                            next_magneto_pos = magneto_pos

                            if jean_pos == jean_action:
                                transition_prob*=(1-self.jeanMovementProb)
                                next_state = next_magneto_pos + wolverine_pos + jean_pos
                            else:
                                transition_prob*=self.jeanMovementProb
                                next_state = next_magneto_pos + wolverine_pos + jean_action
                            

                            if self.isEndState[next_state] == True:
                                q_sa += transition_prob*(self.states[next_state] + 0)
                            else:
                                q_sa += transition_prob*(0 + self.states[next_state]*self.discount)
                    
                        possible_s.append(q_sa)
                        possible_act.append(action)
                states_temp[key] = max(possible_s)
                idx = possible_s.index(max(possible_s))
                self.policy[key] = possible_act[idx]
            
            for key in self.states.keys():
                if abs(states_temp[key] - self.states[key]) > self.converge_eps:
                    converged = False
            if converged == True:
                print("Converged")
                break
            self.states = copy.deepcopy(states_temp)

        # for key in self.states.keys():
        #     print(key, self.states[key], self.policy[key])

    def getNextMove(self, magneto_pos, wolverine_pos, jean_pos):
        state = magneto_pos + wolverine_pos + jean_pos
        return self.policy[state]

def findWinner(jeanPosition, magnetoPosition, wolverinePosition):
    if jeanPosition != magnetoPosition and magnetoPosition == wolverinePosition:
        # print("Magneto Wins")
        return -1
    elif jeanPosition == magnetoPosition and magnetoPosition == wolverinePosition:
        # print("Draw")
        return 0
    elif jeanPosition == wolverinePosition and wolverinePosition!=magnetoPosition:
        # print("Wolverine Wins")
        return 1
    return -100

def drawBoard(jeanPosition, magnetoPosition, wolverinePosition):
    print("Jean Position:", jeanPosition)
    print("Magneto Position:", magnetoPosition)
    print("Wolverine Position", wolverinePosition)
    l = [0]*grid_dim
    grid = []
    for _ in range(grid_dim):
        grid.append(copy.deepcopy(l))

    grid[jeanPosition[0]-1][jeanPosition[1]-1] = 'J'
    grid[wolverinePosition[0] - 1][wolverinePosition[1] - 1] = 'W'
    grid[magnetoPosition[0] - 1][magnetoPosition[1] - 1] = 'M'
    grid[blocked_square[0] - 1][blocked_square[1] - 1] = '-1'
    grid[xavier_school[0] - 1][xavier_school[1] - 1] = 'X'

    for i in range(grid_dim):
        for j in range(grid_dim):
            print(grid[i][j], end = " ")
        print()
    print()

def trials(mdp, num_trials = 100000):
    num_wolverine_wins = 0
    num_draws = 0
    num_magneto_wins = 0

    for _ in tqdm(range(num_trials)):
        max_iter = int(1e6)
        jean = Jean()
        magneto = ActiveMagneto()

        jeanPosition = jean.getCurrentPosition()
        magnetoPosition = magneto.getCurrentPosition()
        wolverinePosition = (randint(1, 5), randint(1, 5))
        while True:
            if checkValidMoveWolverine(wolverinePosition) == False:
                wolverinePosition = (randint(1, 5), randint(1, 5))
            else:
                break
        
        total_iterations = 0
        for _ in range(max_iter):
            result = findWinner(jeanPosition, magnetoPosition, wolverinePosition)
            if result == -100:
                total_iterations+=1
                # drawBoard(jeanPosition, magnetoPosition, wolverinePosition)
                jean.nextMove()
                magneto.nextMove(wolverinePosition)
                jeanPosition = jean.getCurrentPosition()
                magnetoPosition = magneto.getCurrentPosition()
                next_move = mdp.getNextMove(magnetoPosition, wolverinePosition, jeanPosition)
                # print(next_move)
                if next_move is not None:
                    wolverine_next_position = tuple(map(lambda i, j: i + j, wolverinePosition, next_move))
                    if randint(1, 20)<=19:
                        wolverinePosition = wolverine_next_position

            elif result ==-1:
                num_magneto_wins+=1
                break
            elif result == 0:
                num_draws+=1
                break
            else:
                num_wolverine_wins+=1
                break
    
    print(num_wolverine_wins*100/num_trials)
    print(num_draws*100/num_trials)
    print(num_magneto_wins*100/num_trials)
    avg_reward = num_wolverine_wins*20 + num_magneto_wins*-20 + num_draws*-15
    print(avg_reward/num_trials)
    print(total_iterations/num_trials)

def playGame(mdp):
    max_iter = int(1e6)
    jean = Jean()
    magneto = ActiveMagneto()

    jeanPosition = jean.getCurrentPosition()
    magnetoPosition = magneto.getCurrentPosition()
    wolverinePosition = (randint(1, 5), randint(1, 5))
    while True:
        if checkValidMoveWolverine(wolverinePosition) == False:
            wolverinePosition = (randint(1, 5), randint(1, 5))
        else:
            break
    print("Initial Board")
    drawBoard(jeanPosition, magnetoPosition, wolverinePosition)
    result = findWinner(jeanPosition, magnetoPosition, wolverinePosition)
    for iter_num in range(max_iter):
        result = findWinner(jeanPosition, magnetoPosition, wolverinePosition)
        if result == -100:
            jean_next_position = jean.nextMove()
            magneto_next_position = magneto.nextMove(wolverinePosition)
            result = findWinner(jean_next_position, magneto_next_position, wolverinePosition)
            if result != -100:
                drawBoard(jean_next_position, magneto_next_position, wolverinePosition)
                break
            next_move = mdp.getNextMove(magnetoPosition, wolverinePosition, jeanPosition)
            # print(next_move)
            if next_move is not None:
                wolverine_next_position = tuple(map(lambda i, j: i + j, wolverinePosition, next_move))
                if randint(1, 20)<=19:
                    wolverinePosition = wolverine_next_position

            jeanPosition = jean.getCurrentPosition()
            magnetoPosition = magneto.getCurrentPosition()
            print("After move", iter_num+1)
            drawBoard(jeanPosition, magnetoPosition, wolverinePosition)
        else:
            break
    if result ==-1:
        print("Magneto Wins")
    elif result == 0:
        print("Draw")
    elif result == 1:
        print("Wolverine Wins")
    else:
        print("Iterations Ended")

if __name__ == "__main__":
    mdp = MDP()
    mdp.train()
    playGame(mdp)
    # trials(mdp)





