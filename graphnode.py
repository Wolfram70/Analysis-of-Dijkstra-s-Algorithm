class GraphNode:

	def __init__(self, i) -> None:
		self.id = i
		self.dist = float('inf')
		self.adj = []
		self.prev = None
		self.node = None

	def updatePrev(self, g):
		self.prev = g

	def updateDist(self, d):
		self.dist = d
	
	def addedge(self, n, w):
		self.adj.append([n, w])

	def connectNode(self, n):
		self.node = n