import random
import copy
import math
import numpy as np
from tqdm import tqdm
from matplotlib import pyplot as plt
seed = 2
np.random.seed(seed)
random.seed(seed)

fitness_list = []

#this function calculates number of attacking pairs
def fitness(individual):
    n = len(individual)
    horizontal_attacks = 0
    for i in range(n):
        for j in range(n):
            if i!=j and individual[i]== individual[j]:
                horizontal_attacks+=1
    horizontal_attacks//=2

    diagonal_attacks = 0
    for i in range(n):
        for j in range(n):
            if i!=j:
                if abs(i-j) == abs(individual[i] - individual[j]):
                    diagonal_attacks+=1
    diagonal_attacks//=2
    return horizontal_attacks + diagonal_attacks
    

    

def crossover(individual1, individual2):
    n = len(individual1)
    pos = np.random.randint(0, n-1)
    return individual1[:pos] + individual2[pos:], individual2[:pos] + individual1[pos:]


def mutation(individual):
    pos = np.random.randint(0, len(individual)-1)
    individual[pos] = np.random.randint(1, len(individual))
    return individual

def generate_individual(n):
    result = list(range(1, n + 1))
    np.random.shuffle(result)
    return result

class Genetic(object):

    def __init__(self, n ,pop_size):
        #initializing a random individuals with size of initial population entered by user
        self.queens = []
        for i in range(pop_size):
            self.queens.append(generate_individual(n))
        self.max_fitness = int(n*(n-1)/2)
        self.n = n
        self.pop_size = pop_size
    #generating individuals for a single iteration of algorithm
    def generate_population(self, random_selections=5, mutation_prob = 0.3, crossover_prob = 0.3):
        parent = []
        parent_fitness =[]
        #getting individuals from queens randomly for an iteration
        for i in range(random_selections):
            idx = random.randint(0, len(self.queens) - 1)
            parent.append(self.queens[idx])
            parent_fitness.append(fitness(self.queens[idx]))
        
        sort_idx = np.argsort(np.array(parent_fitness))
        parent1 = parent[sort_idx[0]]
        parent2 = parent[sort_idx[1]]

        if parent1 != parent2:
            child1, child2 = crossover(parent1, parent2)
        else:
            parent2 = generate_individual(self.n)
            child1, child2 = crossover(parent1, parent2)
            


        if random.random()< mutation_prob:
            child1 = mutation(child1)
        if random.random()< mutation_prob:
            child2 = mutation(child2)

        self.queens.append(child1)
        self.queens.append(child2)
        queen_fitness = []
        for i in self.queens:
            queen_fitness.append(fitness(i))

        sort_idx = np.argsort(np.array(queen_fitness))
        self.queens.pop(sort_idx[-1])        
        queen_fitness.pop(sort_idx[-1])
        sort_idx = np.argsort(np.array(queen_fitness))
        self.queens.pop(sort_idx[-1])        
        queen_fitness.pop(sort_idx[-1])
        sort_idx = np.argsort(np.array(queen_fitness))

    def finished(self):
        global fitness_list
        mini = int(1e9)
        for i in self.queens:
            #we check if for each queen there is no attacking(cause this algorithm should work for n queen,
            # it was easier to use attacking pairs for fitness instead of non-attacking)
            fit = fitness(i)
            mini = min(fit, mini)
            if fit == 0:
                fitness_list.append(mini)
                return True, i
        fitness_list.append(mini)
        return False, 0

    def start(self, random_selections=5, max_iter = int(1e7), crossover_prob = 0.1, mutation_prob = 0.1):
        #generate new population and start algorithm until number of attacking pairs is zero
        for idx in tqdm(range(max_iter)):
            chk, idx = self.finished()
            if chk == False:
                self.generate_population(random_selections, mutation_prob, crossover_prob)
            else:
                print('Solution: ', idx)
                break



n=(int)(input('Enter the value of N -'))
initial_population= (int)(input('Enter initial population size -'))
mutation_prob = (float)(input('Enter mutation prob -'))
crossover_prob = (float)(input('Enter crossover prob -'))
# n=8
# initial_population= 2
# mutation_prob = 0.1
# crossover_prob = 0.1

algorithm = Genetic(n=n,pop_size=initial_population)
algorithm.start(random_selections=5, mutation_prob= mutation_prob, crossover_prob = crossover_prob)
# legend_list = []
# for i in range(2, 8):
#     seed = 2
#     np.random.seed(seed)
#     random.seed(seed)
#     mutation_prob = i/10

#     fitness_list = []
#     algorithm = Genetic(n=n,pop_size=initial_population)
#     algorithm.start(random_selections=5, mutation_prob= mutation_prob, crossover_prob = crossover_prob)
#     plt.plot(fitness_list)
#     legend_list.append("Mutation Prob. is " + str(mutation_prob))

# plt.legend(legend_list)

# plt.xlabel('Number of Generations')
# plt.ylabel('Fitness')
# plt.show()
