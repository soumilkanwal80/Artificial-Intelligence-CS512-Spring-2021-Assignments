import random, numpy as np, copy
random.seed(0)
np.random.seed(0)

from matplotlib import pyplot as plt

mu = [1, 2]

def probX1GivenX2(a, x2):
    return np.random.normal((mu[0] + a*(x2 - mu[1])), 1 - a**2)

def probX2GivenX1(a, x1):
    return np.random.normal((mu[1] + a*(x1 - mu[0])), 1 - a**2)

def getSamples(a, num_samples = 10000):

    x1 = random.random()
    x2  = random.random()

    x1_samples = [x1]
    x2_samples = [x2]
    for _ in range(num_samples):
        x1_samples.append(probX1GivenX2(a, x2_samples[-1]))
        x2_samples.append(probX2GivenX1(a, x1_samples[-1]))
    
    return x1_samples[1:], x2_samples[1:]

#np.random.multivariate_normal
def getCovarianceMatrix(a):
    return np.array([
        [1, a],
        [a, 1]
    ])

def gibbsSampler(a):    
    fig, axs = plt.subplots(2, 2)
    fig.canvas.set_window_title('a = ' + str(a)) 
    x1_sampled, x2_sampled = getSamples(a)
    x1_actual, x2_actual = np.random.multivariate_normal(mu, getCovarianceMatrix(a), 10000).T

    axs[0, 0].plot(x1_sampled, x2_sampled)
    axs[0, 0].set_title('Gibbs Sampler')
    axs[0, 0].set(xlabel = 'x1', ylabel = 'x2')
    axs[0, 1].plot(x1_actual, x2_actual)
    axs[0, 1].set(xlabel = 'x1', ylabel = 'x2')
    axs[0, 1].set_title('Actual')
    axs[1, 0].plot(x1_sampled)
    axs[1, 0].set_title('Traceplot x1')
    axs[1, 0].set(xlabel = 'Number of Samples', ylabel = 'x1')
    axs[1, 1].plot(x2_sampled)
    axs[1, 1].set_title('Traceplot x2')
    axs[1, 1].set(xlabel = 'Number of Samples', ylabel = 'x2')
    plt.show()

if __name__ == "__main__":
    gibbsSampler(a = 0)
    gibbsSampler(a = 0.99)
    


