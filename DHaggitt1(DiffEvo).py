import random
import numpy as np
import math

# Constants declared for camera padding (to account for any distortion)
INNER_PADDING=0.5
OUTER_PADDING=1.5
FRONT_PADDING=0.75

# Crossover Algorithm
def Crossover(v, w):
  l = len(v)
  p = 1/l
  swapFlag = False
  while(not swapFlag):
    for i in range(l):
      if p >= random.uniform(0, 1):
        temp = v[i]
        v[i] = w[i]
        w[i] = temp
        swapFlag = True
  if(random.random() <= 0.5):
    return v
  else:
    return w

# DistanceFromDestination Function - Calculates distance from location to destination in cm
def DistanceFromDestination(location, destination):
  sum = 0
  for i in range(len(destination)):
    sum += (destination[i] - location[i]) ** 2
  distanceToDest = math.sqrt(sum)
  return distanceToDest

# Fitness Function
def Fitness(source, vector, destination, depth, center):
  location = source + vector
  sum = 0
  for i in range(len(vector)):
    sum += (destination[i] - location[i]) ** 2
  distance = math.sqrt(sum)
  distanceToDest = DistanceFromDestination(source, destination)
  zcoord = np.array([vector[2] * INNER_PADDING, vector[2] * OUTER_PADDING]).astype(int)
  zcoord = np.sort(zcoord + center[0])
  ycoord = np.array([vector[1] * INNER_PADDING, vector[1] * OUTER_PADDING]).astype(int)
  ycoord = np.sort(ycoord + center[1])
  if(np.all(zcoord < len(depth[0])) and np.all(zcoord > 0) and np.all(ycoord < len(depth)) and np.all(ycoord > 0)):
    output = (distanceToDest - distance) / distanceToDest
    if(np.any((depth[ycoord].T[zcoord] * FRONT_PADDING) < vector[0])):
      output = -distance * 10
  else:
    output = -distance * 5
  return (distanceToDest - distance) / distanceToDest

# Differential Evolution Algorithm
def DifferentialEvolution(source, mutateRate, popsize, destination, depth):
  # Initialize variables that will be used internal to the function
  goodMove = True
  center = np.array([int(len(depth) * 0.5), int(len(depth[0]) * 0.5)])
  P = [0] * popsize
  Q = []
  Best = np.array([])
  t = 1
  maxIter = 20

  # Create a set of random vectors
  for i in range(popsize):
    a = random.uniform(-20, 20)
    b = random.uniform(-20, 20)
    c = random.uniform(-20, 20)
    P[i] = np.array([a, b, c])

  # Use genetic algorithms to create a population of best vectors
  while(t <= maxIter and (Best.size == 0 or (np.linalg.norm(Best) < 50 and DistanceFromDestination(source + Best, destination) > 20))):
    # Calculate fitness of each vector and its parent, and keep the best vector
    index = 0
    for Pi in P:
      PFit = Fitness(source, Pi, destination, depth, center)
      if Q and (Fitness(source, Q[index], destination, depth, center) > PFit):
        Pi = Q[index]
      if Best.size == 0 or PFit > Fitness(source, Best, destination, depth, center):
        Best = Pi
      index += 1
    Q = P

    # Mutate the population of vectors to create child vectors
    index = 0
    for Qi in Q:
      a = Q[random.randint(1, popsize) - 1]
      while np.array_equal(Qi, a):
        a = Q[random.randint(1, popsize) - 1]
      b = Q[random.randint(1, popsize) - 1]
      while np.array_equal(Qi, b) or np.array_equal(b, a):
        b = Q[random.randint(1, popsize) - 1]
      c = Q[random.randint(1, popsize) - 1]
      while np.array_equal(Qi, c) or np.array_equal(c, a) or np.array_equal(c, b):
        c = Q[random.randint(1, popsize) - 1]
      d = a + mutateRate * (b - c)
      P[index] = Crossover(d, np.copy(Qi))
      index += 1;
    
    # Increment to the next generation
    t += 1
  
  # Set the coordinates according to the best vector
  zcoord = Best[2] + center[0]
  ycoord = Best[1] + center[1]

  # If best vector is outside of current vision, report bad move
  if(0 < zcoord and zcoord < len(depth) and 0 < ycoord and ycoord < len(depth[0])):
    if(Best[0] > (depth[int(zcoord)][int(ycoord)] * FRONT_PADDING)):
        goodMove = False
  return Best, goodMove
