import numpy as np
from random import seed, choice, randint, random
from tqdm import tqdm
import copy
import math
seed(0)
cavemanMovesList = [(0, 0), (1, 0), (0, 1), (-1, 0), (0, -1)]
grid_dim = 8
sheepMovesList = [(1, 1), (-1, -1), (1, -1), (-1, 1), (0, 0), (2, 2), (-2, -2), (-2, 2), (2, -2)]
cavemanRandomMoveProb = 0.2

#caveman1 is moving 
def checkCavemenValidMove(caveman1_pos, caveman2_pos, sheep_pos):
    if caveman1_pos[0]>=0 and caveman1_pos[0]<grid_dim and caveman1_pos[1] >= 0 and caveman1_pos[1]<grid_dim and caveman1_pos!=caveman2_pos:
        return True
    return False


def checkSheepValidMove(caveman1_pos, caveman2_pos, sheep_pos):
    if sheep_pos[0]>=0 and sheep_pos[0]<grid_dim and sheep_pos[1] >= 0 and sheep_pos[1]<grid_dim:
        return True
    return False


def addTuples(t1, t2):
    return (t1[0] + t2[0], t1[1] + t2[1])

class Caveman:
    def __init__(self, caveman2_pos = None, sheep_pos = None):
        self.pos = (randint(0, grid_dim - 1), randint(0, grid_dim - 1))
        
        if caveman2_pos is not None:
            while self.pos == sheep_pos or self.pos == caveman2_pos :
                self.pos = (randint(0, grid_dim - 1), randint(0, grid_dim - 1))
        else:
            while self.pos == sheep_pos:
                self.pos = (randint(0, grid_dim - 1), randint(0, grid_dim - 1))

    def euclideanDistance(self, new_caveman_pos, sheep_pos):
        return math.sqrt((new_caveman_pos[0] - sheep_pos[0])**2 + (new_caveman_pos[1] - sheep_pos[1])**2)
    
    def getNextMove(self, other_caveman_pos, sheep_pos):
        # if randint(1, 10)<=2:
        if random()<cavemanRandomMoveProb:
            possible_moves = []
            for move in cavemanMovesList:
                temp = addTuples(self.pos, move)
                if checkCavemenValidMove(temp, other_caveman_pos, sheep_pos) == True:
                    possible_moves.append(move)
            move = choice(possible_moves)
            self.pos = addTuples(move, self.pos)
            return self.pos
        else:
            possible_moves = []
            dist_after_move = []
            for move in cavemanMovesList:
                temp = addTuples(self.pos, move)
                if checkCavemenValidMove(temp, other_caveman_pos, sheep_pos) == True:
                    possible_moves.append(move)
                    dist_after_move.append(self.euclideanDistance(temp, sheep_pos))


            idx = dist_after_move.index(min(dist_after_move))
            self.pos = addTuples(possible_moves[idx], self.pos)
            return self.pos
    def getCurrentPosition(self):
        return self.pos


class Sheep:
    def __init__(self):
        self.pos = (randint(0, grid_dim - 1), randint(0, grid_dim - 1))
    
    def euclideanDistance(self, pos1, pos2):
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

    def getDistance(self, sheep_next_pos, caveman1_pos, caveman2_pos):
        dist = self.euclideanDistance(sheep_next_pos, caveman1_pos) \
                + self.euclideanDistance(sheep_next_pos, caveman2_pos) \
                    + min( \
                            self.euclideanDistance(sheep_next_pos, (0, 0)), \
                            self.euclideanDistance(sheep_next_pos, (0, grid_dim-1)),\
                            self.euclideanDistance(sheep_next_pos, (grid_dim-1, 0)), \
                            self.euclideanDistance(sheep_next_pos, (grid_dim- 1, grid_dim-1)) \
                            )
        return dist

    def getNextMove(self, caveman1_pos, caveman2_pos):
        if self.euclideanDistance(caveman1_pos, self.pos)>2 and self.euclideanDistance(caveman2_pos, self.pos)>2:
            return self.pos

        possible_moves = []
        dist_after_moves = []
        for move in sheepMovesList:
            temp = addTuples(self.pos, move)
            if checkSheepValidMove(caveman1_pos, caveman2_pos, temp) == True:
                possible_moves.append(move)
                dist_after_moves.append(self.getDistance(temp, caveman1_pos, caveman2_pos))

        idx = dist_after_moves.index(max(dist_after_moves))
        self.pos = addTuples(possible_moves[idx], self.pos)
        return self.pos
    
    def getCurrentPosition(self):
        return self.pos


def drawGrid(sheep_pos, caveman1_pos, caveman2_pos):
    print("Sheep Position:", sheep_pos)
    print("Caveman 1: Position:", caveman1_pos)
    print("Caveman 2: Position:", caveman2_pos)
    l = [0]*grid_dim
    grid = []
    for _ in range(grid_dim):
        grid.append(copy.deepcopy(l))

    grid[sheep_pos[0]][sheep_pos[1]] = 'S'
    grid[caveman1_pos[0]][caveman1_pos[1]] = 'C1'
    grid[caveman2_pos[0]][caveman2_pos[1]] = 'C2'
    
    for i in range(grid_dim):
        for j in range(grid_dim):
            print(grid[i][j], end = " ")
        print()
    print()

def playGame(max_iter = 200):
    sheep = Sheep()
    caveman1 = Caveman(sheep_pos=sheep.getCurrentPosition())
    caveman2 = Caveman(caveman2_pos=caveman1.getCurrentPosition(), sheep_pos=sheep.getCurrentPosition)


    sheep_pos = sheep.getCurrentPosition()
    caveman1_pos = caveman1.getCurrentPosition()
    caveman2_pos = caveman2.getCurrentPosition()
    drawGrid(sheep_pos, caveman1_pos, caveman2_pos)

    for _ in range(max_iter):
        sheep_pos_new = sheep.getNextMove(caveman1_pos, caveman2_pos)
        caveman1_pos_new = caveman1.getNextMove(caveman2_pos, sheep_pos)
        if caveman1_pos_new == sheep_pos_new:
            drawGrid(sheep_pos_new, caveman1_pos_new, caveman2_pos)
            print("Caveman 1 Wins")
            return 0
        caveman2_pos_new = caveman2.getNextMove(caveman1_pos, sheep_pos)
        if caveman2_pos_new == sheep_pos_new:
            drawGrid(sheep_pos_new, caveman1_pos_new, caveman2_pos_new)
            print("Caveman 2 Wins")
            return 1
        sheep_pos = sheep.getCurrentPosition()
        caveman1_pos = caveman1.getCurrentPosition()
        caveman2_pos = caveman2.getCurrentPosition()  
        drawGrid(sheep_pos, caveman1_pos, caveman2_pos)
    print("Sheep Wins")
    return 2

if __name__ == "__main__":
    cnt = [0, 0, 0]
    for _ in range(5):
        res = playGame()
        cnt[res]+=1
    print("Caveman 1 Wins:", cnt[0], "games")
    print("Caveman 2 Wins:", cnt[1], "games")
    print("Sheep Wins:", cnt[2], "games")






