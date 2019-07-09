import numpy as np
import math
import matplotlib.pyplot as plt
ax = plt.axes()

def initVectors(radii):
    vectors = []
    for r in radii:
        vectors.append([r, 0])
    return vectors

def calcCost(radii, angles):
    return True

def calcTip(tail, radius, theta):
    x = tail[0] + radius * math.cos(theta)
    y = tail[1] + radius * math.sin(theta)
    return [x, y]

'''
calculates the vector sum of multiple vectors
@param vectors - all the vectors to be summed, in the following format:
    [[r0, theta0], [r1, theta1], ...]
'''
def vectorSum(vectors):
    tail = [0, 0]
    for v in vectors:
        tail = calcTip(tail, v[0], v[1])
    return np.array([round(tail[0],3), round(tail[1],3)])

def draw(vectors):
    tail = [0, 0]
    for v in vectors:
        tip = calcTip(tail, v[0], v[1])
        dx = tip[0] - tail[0]
        dy = tip[1] - tail[1]
        ax.arrow(tail[0], tail[1], dx, dy)
        tail = tip

def getMagnitude(vector):
    total = 0
    for i in vector:
        total = total + i**2
    return math.pow(total, 1/len(vector))

def goToMagnitude(dest, iterations):
    theta = 0
    leastError = getMagnitude(vectorSum(vectors) - dest)
    bestTheta = theta
    step = math.pi/2

    for n in range(len(vectors)):
        while (theta < 2*math.pi):
            vectors[n][1] = theta
            end = vectorSum(vectors)
            error = getMagnitude(end - dest)
            if (error < leastError):
                leastError = error
                bestTheta = theta
            theta = theta + step
        vectors[n][1] = bestTheta
        theta = 0
        leastError = getMagnitude(vectorSum(vectors) - dest)
        bestTheta = theta
    errorHistory[0].append(0)
    errorHistory[1].append(leastError)

    for i in range(1, iterations):
        print(i)
        for n in range(len(vectors)):
            bestTheta = vectors[n][1]
            theta = bestTheta - step * 2            
            upperLimit = bestTheta + step * 2
            while (theta < upperLimit):
                vectors[n][1] = theta
                end = vectorSum(vectors)
                error = getMagnitude(end - dest)
                if (error < leastError):
                    leastError = error
                    bestTheta = theta
                theta = theta + step
            vectors[n][1] = bestTheta
            leastError = getMagnitude(vectorSum(vectors) - dest)
        try:
            stepScaleFactor = (leastError / errorHistory[1][i-1])
        except ZeroDivisionError:
            return vectors
        if (stepScaleFactor == 1):
            stepScaleFactor = 0.5
        step = step * stepScaleFactor
        errorHistory[0].append(i)
        errorHistory[1].append(leastError)

    return vectors

destination = np.array([-17, 13.96])
errorHistory = [[], []]
vectors = initVectors([15, 2, 6, 3.5])
maxLength = np.sum(vectors, axis=0)[0]
print(vectors)

iterations = 50
result = goToMagnitude(destination, iterations)
print("result:", result)
print("least error:", errorHistory[1][-1])

plt.xlim(-1.1*maxLength, 1.1*maxLength)
plt.ylim(-1.1*maxLength, 1.1*maxLength)
plt.grid(alpha = 0.25)
plt.scatter(destination[0], destination[1])
draw(result)

plt.figure(num="Iterations vs Error")
plt.plot(errorHistory[0], errorHistory[1])

plt.show()