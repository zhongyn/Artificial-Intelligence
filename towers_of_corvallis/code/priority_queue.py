from heapq import *

class PriorityQueue(object):
    """Implementation of priority queue with heap queue."""
    def __init__(self):
        self.pq = []
        self.entryfinder = {}

    def contain(self, state):
        if state.name in self.entryfinder:
            return True
        return False

    def isempty(self):
        if not self.pq:
            return True
        return False

    def add(self, state):
        self.entryfinder[state.name] = state
        heappush(self.pq, state)

    def pop(self):
        state = heappop(self.pq)
        del self.entryfinder[state.name]
        return state

    def getpriority(self, state):
        return self.entryfinder[state.name].priority

    def setpriority(self, state):
        self.entryfinder[state.name].priority = state.priority
        heapify(self.pq)



