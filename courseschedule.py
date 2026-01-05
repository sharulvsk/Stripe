from collections import deque, defaultdict

class Solution:
    def canFinish(self, numCourses: int, prerequisites: list[list[int]]) -> bool:
        graph = defaultdict(list)
        indegree = [0] * numCourses

        # Build graph + indegree array
        for a, b in prerequisites:   # b -> a (take b before a)
            graph[b].append(a)
            indegree[a] += 1

        # Start with courses having no prerequisites
        q = deque([i for i in range(numCourses) if indegree[i] == 0])
        taken = 0

        while q:
            course = q.popleft()
            taken += 1

            for nei in graph[course]:
                indegree[nei] -= 1
                if indegree[nei] == 0:
                    q.append(nei)

        # If we processed all courses, no cycle exists
        return taken == numCourses
    