import numpy as np
import copy
from tqdm import tqdm
from random import randint, seed, choice, random
# seed(0)

numStates = 6
numObservations = 16
numSensors = 4
sensorAccuracy = 0.75

# takes a binary string and converts it to integer
def stringToInteger(s):
    assert len(s) == numSensors
    l = len(s)
    mul = 1
    sum_num = 0
    for i in range(l):
        sum_num+=(ord(s[l-i-1]) - ord('0'))*mul
        mul*=2
    return sum_num


environmentReadings = [
    stringToInteger('1000'), stringToInteger('0110'), \
        stringToInteger('0111'), stringToInteger('0011'), \
            stringToInteger('1000'), stringToInteger('1000')
]

transitionMatrix = np.array([
    [0.2, 0.8, 0, 0, 0, 0],
    [0.4, 0.2, 0.4, 0, 0, 0],
    [0, 0.26, 0.2, 0.27, 0.27, 0],
    [0, 0, 0.4, 0.2, 0.4, 0],
    [0, 0, 0, 0.8, 0.2, 0],
    [0, 0, 0.8, 0, 0, 0.2]
], dtype= np.float32)


#Generates a path followed by robot of length 100 also generates sensor readings 
def getRandomObservation(timeSteps):
    # get an initial random observation
    cumulativeTransitionMatrix = np.cumsum(transitionMatrix, axis = 1)
    curr_state = randint(0, numStates - 1)
    actual_path = []
    sensorReading=[getObservationForState(curr_state)]

    actual_path.append(curr_state)
    for t in range(1, timeSteps):
        prob = random()
        l = 0
        r = cumulativeTransitionMatrix[curr_state][0]
        for i in range(1, numStates):
            if l<=prob and prob<r:
                #move with 80% probabbility
                if randint(1, 10)<=8:
                    curr_state = i
                break
            l = r
            r = cumulativeTransitionMatrix[curr_state][i]
        sensorReading.append(getObservationForState(curr_state))
        actual_path.append(curr_state)

    return actual_path,sensorReading

#Get emission probability by calculating bit difference between actual and observed readings
def getEmissionProbability(actual, observed):
    prob = 1
    for _ in range(numSensors):
        if actual%2==observed%2:
            prob *= sensorAccuracy
        else:
            prob*= (1-sensorAccuracy)
        actual = actual//2
        observed = observed//2
    return prob
    
# Generate Emission Matrix
def getEmissionMatrix():
    emissionMatrix = np.zeros((numStates, numObservations), dtype=np.float32)
    for i in range(numStates):
        for j in range(numObservations):
            emissionMatrix[i][j] = getEmissionProbability(environmentReadings[i], j)
    return emissionMatrix


emissionMatrix = getEmissionMatrix()
#probability that robot starts in i-th state 
initialProbabilities = [1/numStates]*numStates

# Returns randomly modified sensor readings
def getObservationForState(state):
    actual = environmentReadings[state]
    actual_binary = []
    while(len(actual_binary)<numSensors):
        actual_binary.append(actual%2)
        actual//=2
    
    for i in range(len(actual_binary)):
        if randint(1, 4) == 4:
            actual_binary[i] = 1 - actual_binary[i]
    
    mul = 1
    observed = 0
    for i in range(len(actual_binary)):
        observed+=actual_binary[i]*mul
        mul*=2
    return observed

# Update B for every time steo
def updateB(curr_observation, B):
    B_prime = [0]*numStates
    for i in range(numStates):
        sum_prob =0
        for j in range(numStates):
             sum_prob+= B[j]*transitionMatrix[j][i]
        B_prime[i] = sum_prob
    for i in range(numStates):
        B_prime[i]=B_prime[i]*emissionMatrix[i][curr_observation]
    
    x = sum(B_prime)
    for i in range(numStates):
        B_prime[i] /= x
    return B_prime
    
# Calucates viterbi path
def viterbi2(time, observations):
    B = copy.deepcopy(initialProbabilities)
    probability = []
    predicted = []
    for t in range(time):
        B = updateB(observations[t], B)
        idx = B.index(max(B))
        probability.append(max(B))
        predicted.append(idx)
    return predicted, probability


def trials(max_iter = 1000):
    accuracy = []
    t = 100
    for _ in tqdm(range(max_iter)):
        actual_path, sensorReading = getRandomObservation(t)
        predicted = viterbi2(t, sensorReading)
        sum1 = 0
        for i in range(t):
            sum1+=actual_path[i] == predicted[i]
        accuracy.append(sum1/t)

    print(sum(accuracy)/len(accuracy))

if __name__ == "__main__":
    t = 100
    actual_path, sensorReading = getRandomObservation(t)
    predicted, probability = viterbi2(t, sensorReading)
    sum1 = 0
    for i in range(t):
        sum1+=actual_path[i] == predicted[i]
    print("Timestep", "Predicted", "Actual", "Probability")
    for i in range(1, t + 1):
        if i%10 == 0:
            print(i, "\t",  predicted[i-1], "\t\t", actual_path[i-1], round(probability[i-1], 2))
    print("Accuracy of Prediction is:", sum1*100/t, "%")
