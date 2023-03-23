import math
from fibheap import FibonacciHeap
from priorityqueue import MinHeapPriorityQueue
from graphnode import GraphNode

class Graph:

	def __init__(self, adj):
		self.num = len(adj)
		self.nodes = []
		for i in range(0, self.num):
			self.nodes.append(GraphNode(i))
		for (i, row) in enumerate(adj):
			for(j, ele) in enumerate(row):
				if ele != 0:
					self.nodes[i].addedge(self.nodes[j], ele)
	
	F = FibonacciHeap()
	P = MinHeapPriorityQueue()

	def check(self):
		for node in self.nodes:
			for v,w in node.adj:
				print(str(node.id) + ':' + str(v.id) + ',' + str(w))

	def Initialize(self, s, Q):
		for node in self.nodes:
			Q.insert(node)
		Q.decrease_key(s.node, 0, None)
    
	def Relax(self, u, v, w, Q):
		if v.dist > u.dist + w:
			Q.decrease_key(v.node, u.dist + w, u)
	
	def dijkstraF(self, s):
		if s > self.num - 1:
			print('Error: Start node not found')
			return
		S=[]
		self.Initialize(self.nodes[s], self.F)
		while not self.F.isempty():
			u = self.F.extract_min()
			S.append(u.graphNode)
			for v,w in u.graphNode.adj:
				self.Relax(u.graphNode, v, w, self.F)

	def dijkstraP(self, s):
		if s > self.num - 1:
			print('Error: Start node not found')
			return
		S=[]
		self.Initialize(self.nodes[s], self.P)
		while not self.P.isempty():
			u = self.P.extract_min()
			S.append(u)
			for v,w in u.adj:
				self.Relax(u, v, w, self.P)
	
	def printDist(self):
		for node in self.nodes:
			print(node.dist)
	
	def reset(self):
		for node in self.nodes:
			node.dist = float('inf')
			node.prev = None
			node.node = None