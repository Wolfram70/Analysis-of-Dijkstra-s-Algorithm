from graph import Graph
from timeit import default_timer as timer
import numpy as np
import random

size = 1000
iterations = 20
tF = 0
tP = 0

size = int(input('Enter the number of nodes in the graph to simulate Dijkstra\'s algorithm: '))
iterations = int(input('Enter the number of iterations to compute and take average of: '))

for i in range(0, iterations):
	adj = np.zeros((size, size))

	for i in range(0, size):
		for j in range(0, size):
			p = random.random()
			w = int(10 * random.random())
			if w == 0:
				continue
			if p > 0.7:
				adj[i][j] = w
				adj[j][i] = w
	
	for i in range(0, size):
		adj[i][i] = 0

	g = Graph(adj)
	t1 = timer()
	g.dijkstraF(1)
	t2 = timer()
	tF += t2 - t1
	g.reset()
	t1 = timer()
	g.dijkstraP(1)
	t2 = timer()
	tP += t2 - t1

tF /= iterations
tP /= iterations

print('\nAverage time taken (Fibonacci Heap): ' + str(tF) + ' s\nAverage time taken (Minimum Priority Queue): ' + str(tP) + ' s')