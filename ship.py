import heapq
from collections import defaultdict

class Edge:
    def __init__(self, to: str, cost: int):
        self.to = to
        self.cost = cost

def build_graph(input_str: str) -> dict[str, list[Edge]]:
    graph = defaultdict(list)
    routes = input_str.split(':')
    for route in routes:
        parts = route.split(',')
        from_node = parts[0]
        to_node = parts[1]
        cost = int(parts[3])
        graph[from_node].append(Edge(to_node, cost))
    return graph

def find_min_cost(input_str: str, src: str, dest: str) -> int:
    graph = build_graph(input_str)
    pq = [(0, src)]  # (cost, node)
    dist = {src: 0}

    while pq:
        cost, node = heapq.heappop(pq)
        if node == dest:
            return cost
        if node not in graph:
            continue
        for e in graph[node]:
            new_cost = cost + e.cost
            if new_cost < dist.get(e.to, float('inf')):
                dist[e.to] = new_cost
                heapq.heappush(pq, (new_cost, e.to))
    return -1  # no route found

# Example usage
input_str = "US,UK,UPS,5:US,CA,FedEx,3:CA,UK,DHL,7"
print("Direct US → UK cost:", find_min_cost(input_str, "US", "UK"))
