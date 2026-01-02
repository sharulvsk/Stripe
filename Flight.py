from collections import deque, defaultdict

class Solution:
    def findCheapestPrice(self, n, flights, src, dst, k):
        graph = defaultdict(list)
        for u, v, w in flights:
            graph[u].append((v, w))
        dist = [float('inf')] * n
        dist[src] = 0
        q = deque([(src, 0)])
        stops = 0
        while q and stops <= k:
            for _ in range(len(q)):
                node, cost = q.popleft()
                for nei, w in graph[node]:
                    new_cost = cost + w
                    if new_cost < dist[nei]:
                        dist[nei] = new_cost
                        q.append((nei, new_cost))
            stops += 1

        return -1 if dist[dst] == float('inf') else dist[dst]


n = 4
flights = [
    [0, 1, 100],
    [1, 2, 100],
    [2, 3, 100],
    [0, 3, 500]
]
src = 0
dst = 3
k = 1

sol = Solution()
result = sol.findCheapestPrice(n, flights, src, dst, k)
print(result)
