import sys
from collections import defaultdict

def is_small_cave(cave):
    """Returns true if this cave is a small cave."""
    return cave == cave.lower()

def build_graph(edges):
    """Build an adjacency list representation of a graph from a list of edges."""
    graph = defaultdict(list)
    for edge in edges:
        from_vertex, to_vertex = edge.rstrip().split("-")
        graph[from_vertex].append(to_vertex)
        graph[to_vertex].append(from_vertex)
    return graph  

def count_paths(cave_graph, allow_double_visit=False):
    """Count the number of possible paths in the cave."""
    return _count_paths(cave_graph, ["start"], {"start"}, allow_double_visit)

def _count_paths(cave_graph, path, visited_small_caves, allow_double_visit):
    """Recursively count the number of possible paths in the cave."""
    if path[-1] == "end":
        return 1
    num_paths = 0
    for next_cave in cave_graph[path[-1]]:
        next_allow_double_visit = allow_double_visit
        if next_cave in visited_small_caves:
            if not allow_double_visit:
                continue
            elif next_cave == "start":
                continue
            else:
                next_allow_double_visit = False
        next_visited_small_caves = visited_small_caves | {next_cave} if is_small_cave(next_cave) else visited_small_caves    
        path.append(next_cave)
        num_paths += _count_paths(cave_graph, path, next_visited_small_caves, next_allow_double_visit)
        path.pop()
    return num_paths

def main():
    """Advent of Code Day 12."""
    graph = build_graph(sys.stdin.readlines())
    print(count_paths(graph))
    print(count_paths(graph, allow_double_visit=True))

main()
