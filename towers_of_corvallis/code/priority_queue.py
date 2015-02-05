from heapq import *

class PriorityQueue(object):
    """Implementation of priority queue with heap queue."""
    def __init__(self):
        self.pq = []
        self.entryfinder = {}

    def contain(self, node):
        if node.name in self.entryfinder:
            return True
        return False

    def isempty(self):
        if not self.pq:
            return True
        return False

    def add(self, node):
        self.entryfinder[node.name] = node
        heappush(self.pq, node)

    def pop(self):
        while self.pq:
            node = heappop(self.pq)
            if not node.removed:
                del self.entryfinder[node.name]
                return node
        return None

    def remove(self, node):
        self.entryfinder[node.name].removed = True

    def getpriority(self, node):
        return self.entryfinder[node.name].priority

    def getsize(self):
        return len(self.pq)




