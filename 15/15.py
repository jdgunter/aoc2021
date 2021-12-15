import heapq
import sys
import time
from collections import namedtuple
from itertools import count


Graph = namedtuple("Graph", ["weights", "n_rows", "n_cols"])


def neighbors(vertex, graph):
    """Get the neighbors of a vertex in the given graph."""
    i, j = vertex
    if i > 0:
        yield (i-1, j)
    if j > 0:
        yield (i, j-1)
    if i < graph.n_rows - 1:
        yield (i+1, j)
    if j < graph.n_cols - 1:
        yield (i, j+1)


class PQueue:
    """A simple priority queue class."""

    def __init__(self):
        self.pq = []
        self.entries = {}
        self.REMOVED = object()
        self.counter = count()
    
    def add_item(self, item, priority):
        """
        Add an item to the queue.
        
        If the item already exists in the queue with a lower or equal priority,
        do nothing. If it already exists but with a high priority, mark the previous
        entry REMOVED and add an entry with the updated priority.
        """
        if item in self.entries:
            if self.get_priority(item) <= priority:
                return
            self.remove_item(item)
        count = next(self.counter)
        entry = [priority, count, item]
        self.entries[item] = entry
        heapq.heappush(self.pq, entry)
    
    def remove_item(self, item):
        """Mark the given item REMOVED."""
        entry = self.entries.pop(item)
        entry[-1] = self.REMOVED
    
    def get_priority(self, item):
        """Get the current priority of an item."""
        return self.entries[item][0]
    
    def pop(self):
        """Pop the lowest-priority item off the queue."""
        while self.pq:
            priority, _, item = heapq.heappop(self.pq)
            if item is not self.REMOVED:
                del self.entries[item]
                return item, priority
        raise ValueError("No items in queue.")


def min_cost_path(start, end, graph, potential_min_cost_paths=None):
    """Compute the minimum cost path through the graph."""
    min_cost_paths = {start: 0}
    if potential_min_cost_paths is None:
        potential_min_cost_paths = PQueue()
    for vertex in neighbors(start, graph):
        potential_min_cost_paths.add_item(vertex, graph.weights[vertex])

    while end not in min_cost_paths:
        next_min_path, cost = potential_min_cost_paths.pop()
        while next_min_path in min_cost_paths:
            next_min_path, cost = potential_min_cost_paths.pop()
        min_cost_paths[next_min_path] = cost
        for neighbor in neighbors(next_min_path, graph):
            potential_min_cost_paths.add_item(neighbor, graph.weights[neighbor] + cost)

    return min_cost_paths[end]


def taxicab_distance(p, q):
    """Compute the taxicab distance between two points."""
    return abs(p[0] - q[0]) + abs(p[1] - q[1])


def build_big_graph(risk_values, n_rows, n_cols):
    """Build the full graph from the input risk values."""
    new_risk_values = {}
    for block_i in range(5):
        for block_j in range(5):
            for (i,j), risk in risk_values.items():
                new_i, new_j = block_i * n_rows + i, block_j * n_cols + j
                new_risk_values[(new_i, new_j)] = ((risk + taxicab_distance((0, 0), (block_i, block_j)) - 1) % 9) + 1
    return Graph(new_risk_values, n_rows * 5, n_cols * 5)


def main():
    """Advent of Code day 15."""
    risk_values = {}
    for i, line in enumerate(sys.stdin.readlines()):
        for j, risk in enumerate(line.rstrip()):
            risk_values[(i,j)] = int(risk)
    start_time = time.time()

    # Part 1.
    graph = Graph(risk_values, i+1, j+1)
    print(min_cost_path((0,0), (i,j), graph))

    # Part 2.
    big_graph = build_big_graph(risk_values, graph.n_rows, graph.n_cols)
    print(min_cost_path((0, 0), (big_graph.n_rows-1,big_graph.n_cols-1), big_graph))
    print(f"Time: {time.time() - start_time}")
    

main()
