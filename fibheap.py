import math
from graphnode import GraphNode

class FibonacciHeap:

    class Node:
        def __init__(self, n, value):
            self.key = n.dist
            self.graphNode = n
            self.value = value
            self.parent = self.child = self.left = self.right = None
            self.degree = 0
            self.mark = False

    def iterate(self, head):
        node = stop = head
        flag = False
        while True:
            if node == stop and flag is True:
                break
            elif node == stop:
                flag = True
            yield node
            node = node.right

    root_list, min_node = None, None

    total_nodes = 0

    def isempty(self):
        if self.min_node == None:
            return True
        else:
            return False

    def find_min(self):
        return self.min_node

    def extract_min(self):
        z = self.min_node
        if z is not None:
            if z.child is not None:
                children = [x for x in self.iterate(z.child)]
                for i in range(0, len(children)):
                    self.merge_with_root_list(children[i])
                    children[i].parent = None
            self.remove_from_root_list(z)
            if z == z.right:
                self.min_node = self.root_list = None
            else:
                self.min_node = z.right
                self.consolidate()
            self.total_nodes -= 1
        return z

    def insert(self, node, value=None):
        n = self.Node(node, value)
        n.graphNode.connectNode(n)
        n.left = n.right = n
        self.merge_with_root_list(n)
        if self.min_node is None or n.key < self.min_node.key:
            self.min_node = n
        self.total_nodes += 1
        return n

    def decrease_key(self, x, k, prev):
        if k > x.key:
            return None
        x.key = k
        x.graphNode.updateDist(k)
        x.graphNode.updatePrev(prev)
        y = x.parent
        if y is not None and x.key < y.key:
            self.cut(x, y)
            self.cascading_cut(y)
        if x is None or self.min_node is None:
            return None
        if x.key < self.min_node.key:
            self.min_node = x

    def merge(self, h2):
        H = FibonacciHeap()
        H.root_list, H.min_node = self.root_list, self.min_node
        last = h2.root_list.left
        h2.root_list.left = H.root_list.left
        H.root_list.left.right = h2.root_list
        H.root_list.left = last
        H.root_list.left.right = H.root_list
        if h2.min_node.key < H.min_node.key:
            H.min_node = h2.min_node
        H.total_nodes = self.total_nodes + h2.total_nodes
        return H

    def cut(self, x, y):
        self.remove_from_child_list(y, x)
        y.degree -= 1
        self.merge_with_root_list(x)
        x.parent = None
        x.mark = False

    def cascading_cut(self, y):
        z = y.parent
        if z is not None:
            if y.mark is False:
                y.mark = True
            else:
                self.cut(y, z)
                self.cascading_cut(z)

    def consolidate(self):
        A = [None] * int(math.log(self.total_nodes) * 2)
        nodes = [w for w in self.iterate(self.root_list)]
        for w in range(0, len(nodes)):
            x = nodes[w]
            d = x.degree
            if d < len(A):
                while A[d] != None:
                    y = A[d]
                    if x.key > y.key:
                        temp = x
                        x, y = y, temp
                    self.heap_link(y, x)
                    A[d] = None
                    d += 1
                A[d] = x
        for i in range(0, len(A)):
            if A[i] is not None:
                if A[i].key < self.min_node.key:
                    self.min_node = A[i]

    def heap_link(self, y, x):
        self.remove_from_root_list(y)
        y.left = y.right = y
        self.merge_with_child_list(x, y)
        x.degree += 1
        y.parent = x
        y.mark = False

    def merge_with_root_list(self, node):
        if self.root_list is None:
            self.root_list = node
        else:
            node.right = self.root_list.right
            node.left = self.root_list
            self.root_list.right.left = node
            self.root_list.right = node

    def merge_with_child_list(self, parent, node):
        if parent.child is None:
            parent.child = node
        else:
            node.right = parent.child.right
            node.left = parent.child
            parent.child.right.left = node
            parent.child.right = node

    def remove_from_root_list(self, node):
        if node == self.root_list:
            self.root_list = node.right
        node.left.right = node.right
        node.right.left = node.left

    def remove_from_child_list(self, parent, node):
        if parent.child == parent.child.right:
            parent.child = None
        elif parent.child == node:
            parent.child = node.right
            node.right.parent = parent
        node.left.right = node.right
        node.right.left = node.left

    def connectNodes(self):
        a = 5