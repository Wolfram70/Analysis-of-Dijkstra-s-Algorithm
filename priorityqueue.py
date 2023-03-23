from graphnode import GraphNode

class MinHeapPriorityQueue():

    def __init__(self, iterable=(), key=lambda x: x.dist):
        self._key = key
        decorated = [(key(item), item) for item in iterable]
        self._pq = [self.Locator(value, item, i) for i, (value, item) in enumerate(decorated)]
        if len(self._pq) > 1:
            self._heapify()

    class Locator:
        __slots__ = '_value', '_item', '_index'

        def __init__(self, value, item, i):
            self._value = value
            self._item = item
            self._index = i

        def __eq__(self, other):
            return self._value == other._value

        def __lt__(self, other):
            return self._value < other._value

        def __le__(self, other):
            return self._value <= other._value

        def __repr__(self):
            return '{}(value={!r}, item={!r}, index={})'.format(
                self.__class__.__name__,
                self._value,
                self._item,
                self._index
            )

    #------------------------------------------------------------------------------
    # non-public
    def _parent(self, j):
        return (j-1) // 2

    def _left(self, j):
        return 2*j + 1

    def _right(self, j):
        return 2*j + 2

    def _swap(self, i, j):
        self._pq[i], self._pq[j] = self._pq[j], self._pq[i]
        self._pq[i]._index = i
        self._pq[j]._index = j

    def _upheap(self, i):
        parent = self._parent(i)
        if i > 0 and self._pq[i] < self._pq[parent]:
            self._swap(i, parent)
            self._upheap(parent)

    def _downheap(self, i):
        n = len(self._pq)
        left, right = self._left(i), self._right(i)
        if left < n:
            child = left
            if right < n and self._pq[right] < self._pq[left]:
                child = right
            if self._pq[child] < self._pq[i]:
                self._swap(i, child)
                self._downheap(child)

    def _fix(self, i):
        self._upheap(i)
        self._downheap(i)

    def _heapify(self):
        start = self._parent(len(self) - 1)
        for j in range(start, -1, -1):
            self._downheap(j)

    #------------------------------------------------------------------------------
    # public
    def isempty(self):
        if len(self._pq) == 0:
            return True
        else:
            return False
        
    def insert(self, item):
        token = self.Locator(self._key(item), item, len(self._pq))
        self._pq.append(token)
        item.node = token
        self._upheap(len(self._pq) - 1)
        return token

    def decrease_key(self, loc, newval, prev):
        j = loc._index
        item = loc._item
        if not (0 <= j < len(self) and self._pq[j] is loc):
            raise ValueError('Invalid locator')
        loc._value = newval
        loc._item = item
        item.dist = newval
        item.prev = prev
        self._fix(j)

    def remove(self, loc):
        j = loc._index
        if not (0 <= j < len(self) and self._pq[j] is loc):
            raise ValueError('Invalid locator')
        if j == len(self) - 1:
            self._pq.pop()
        else:
            self._swap(j, len(self) - 1)
            self._pq.pop()
            self._fix(j)
        return loc._item

    def peek(self):
        loc = self._pq[0]
        return loc._item

    def extract_min(self):
        self._swap(0, len(self._pq) - 1)
        loc = self._pq.pop()
        self._downheap(0)
        return loc._item

    @property
    def items(self):
        return [token._item for token in self._pq]

    def __len__(self):
        return len(self._pq)

    def __contains__(self, item):
        return item in self.items

    def __iter__(self):
        return iter(sorted(self.items))

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self._pq)