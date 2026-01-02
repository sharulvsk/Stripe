from collections import defaultdict
def calcEquation(equations, values, queries):
    graph = defaultdict(dict)
    for (a, b), val in zip(equations, values):
        graph[a][b] = val
        graph[b][a] = 1 / val
    def dfs(curr, target, visited):
        if curr not in graph or target not in graph:
            return -1.0
        if curr == target:
            return 1.0
        visited.add(curr)
        for neighbor, weight in graph[curr].items():
            if neighbor in visited:
                continue
            res = dfs(neighbor, target, visited)
            if res != -1.0:
                return weight * res
        return -1.0
    results = []
    for a, b in queries:
        results.append(dfs(a, b, set()))
    return results
def main():
    equations = [["a", "b"], ["b", "c"]]
    values = [2.0, 3.0]
    queries = [["a", "c"], ["b", "a"], ["a", "e"], ["a", "a"], ["x", "x"]]

    results = calcEquation(equations, values, queries)
    print(results)
if __name__ == "__main__":
    main()
