from abc import ABC, abstractmethod


class IterativeCompression(ABC):
    def __init__(self, n, k):
        self.n = n
        self.k = k
        self.best_solution = None

    @abstractmethod
    def compress(self, subgraph_nodes, current_solution):
        """
        Try to reduce current_solution (size k+1) to a solution of size k.
        """
        pass

    @abstractmethod
    def get_initial_solution(self, new_vertex, current_solution):
        """
        Logic to extend the current solution when a new vertex is added.
        """
        pass

    def run(self):
        current_nodes = []
        current_solution = set()

        for v in range(self.n):
            current_nodes.append(v)
            # Extend current solution with the new element
            current_solution = self.get_initial_solution(v, current_solution)

            # If solution exceeds k, we must compress it
            if len(current_solution) > self.k:
                compressed = self.compress(current_nodes, current_solution)
                if compressed is None:
                    # If compression fails for a subgraph, no solution exists for k
                    return None
                current_solution = compressed

        self.best_solution = current_solution
        return current_solution


class IterativeCompressionMVC(IterativeCompression):
    def __init__(self, n, k, adj_list):
        super().__init__(n, k)
        self.adj_list = adj_list  # Full adjacency list

    def is_valid_vc(self, T, subgraph_nodes):
        """
        Verifies if T covers all edges within the induced subgraph.
        """
        for u in subgraph_nodes:
            for v in self.adj_list[u]:
                if v in subgraph_nodes:
                    if u not in T and v not in T:
                        return False
        return True

    def get_initial_solution(self, new_vertex, current_solution):
        """
        For MVC, when adding a new vertex, simply add it to the cover.
        """
        new_sol = current_solution.copy()
        new_sol.add(new_vertex)
        return new_sol

    def compress(self, subgraph_nodes, current_cover):
        """
        Implements the 2^(k+1) compression logic for Vertex Cover.
        """
        Slist = list(current_cover)
        size_to_check = len(Slist)  # Should be k+1

        # Iterate over all possible partitions of the current cover
        for sub_id in range(1 << size_to_check):
            T = set()

            # Decision - which nodes from the old cover to keep
            for i in range(size_to_check):
                if (sub_id >> i) & 1 == 1:
                    T.add(Slist[i])

            # For discarded nodes, all their neighbors in the subgraph must be in T
            for i in range(size_to_check):
                if (sub_id >> i) & 1 == 0:
                    discarded_node = Slist[i]
                    for neighbor in self.adj_list[discarded_node]:
                        if neighbor in subgraph_nodes:
                            T.add(neighbor)

            # Check if the new set T is a valid cover and fits size k
            if len(T) <= self.k and self.is_valid_vc(T, subgraph_nodes):
                return T

        return None


def get_petersen_graph():
    # Implementation explained in lab 4
    n = 10
    adj_list = [[] for _ in range(n)]

    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]
    edges += [(5, 7), (7, 9), (9, 6), (6, 8), (8, 5)]
    edges += [(0, 5), (1, 6), (2, 7), (3, 8), (4, 9)]

    for u, v in edges:
        adj_list[u].append(v)
        adj_list[v].append(u)

    return adj_list


if __name__ == '__main__':
    # TASK 1 - small graph
    n, k = 3, 1
    adj = [[1, 2], [0], [0]]

    mvc_solver = IterativeCompressionMVC(n, k, adj)
    result = mvc_solver.run()

    if result:
        print(f"Found Vertex Cover of size {k}: {result}")
    else:
        print(f"No Vertex Cover of size {k} exists.")

    # TASK 2 - Petersen Graph
    n, k = 10, 6
    adj = get_petersen_graph()

    mvc_solver = IterativeCompressionMVC(n, k, adj)
    result = mvc_solver.run()

    if result:
        print(f"Found Vertex Cover of size {k}: {result}")
    else:
        print(f"No Vertex Cover of size {k} exists.")
