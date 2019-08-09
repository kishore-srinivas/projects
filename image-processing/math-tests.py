import numpy
from scipy.misc import derivative
import matplotlib
import matplotlib.pyplot as plt

x = 2 * numpy.random.rand(100, 1)
y = 4 + 3 * x + numpy.random.randn(100, 1)
plt.scatter(x, y)
plt.xlabel('x')
plt.ylabel('y')
plt.title('y as x')
# plt.show()

def calcCost(theta, x, y):
    m = len(y)
    predictions = x.dot(theta)
    cost = (m/2) * numpy.sum(numpy.square(predictions-y))
    return cost

def gradientDescent(x, y, theta, learningRate = 0.01, iterations = 100):
    m = len(y)
    costHistory = numpy.zeros(iterations)
    thetaHistory = numpy.zeros((iterations,2))
    for i in range(iterations):
        prediction = numpy.dot(x,theta)
        # print(theta)
        # print(x.T.dot((prediction-y)))
        # print('-------')
        theta = theta - (1/m) * learningRate * (x.T.dot((prediction-y)))
        thetaHistory[i,:] = theta.T
        costHistory[i] = calcCost(theta, x, y)
    return theta, costHistory, thetaHistory

learningRate = 0.01
iterations = 1000
theta = numpy.random.randn(2,1)
xBiased = numpy.c_[numpy.ones((len(x), 1)), x]
theta, costHistory, thetaHistory = gradientDescent(xBiased, y, theta, learningRate, iterations)

print("theta0:", theta[0][0])
print("theta1:", theta[1][0])
print("final cost:", costHistory[-1])

z = theta[0][0] * x + theta[1][0]
plt.plot(x, z)

plt.figure()
plt.plot(numpy.arange(iterations), costHistory)
plt.show()