from dag import DAG
from collections import deque


def bfs(adj_list, start_node):
    visited = set()
    queue = deque([start_node])
    visited.add(start_node)
    order = []

    while queue:
        u = queue.popleft()
        order.append(u)

        for v in sorted(adj_list[u]):
            if v not in visited:
                visited.add(v)
                queue.append(v)
    return order


def dfs(adj_list, start_node):
    visited = set()
    stack = [start_node]
    order = []

    while stack:
        u = stack.pop()
        if u not in visited:
            visited.add(u)
            order.append(u)

            for v in reversed(sorted(adj_list[u])):
                if v not in visited:
                    stack.append(v)
    return order


dag = DAG(6, 10)

print("BFS:", bfs(dag._get_adjacency_list_representation(), 0))
print("DFS:", dfs(dag._get_adjacency_list_representation(), 0))
