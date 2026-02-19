from abc import ABC, abstractmethod


class LinKernighan(ABC):
    def __init__(self, n, p=3):
        self.n = n
        self.p = p
        self.best_solution = None

    @abstractmethod
    def _get_gain(self, u, v, removing=True):
        """
        Calculates the gain from adding/removing edges."""
        pass

    @abstractmethod
    def _is_valid(self, potential_sol):
        """
        Checks specific constraints of the problem (e.g. is it Hamiltonian cycle)."""
        pass

    @abstractmethod
    def _generate_greedy(self):
        """Generates greedy solution serving as a baseline for improvement."""
        pass

    @abstractmethod
    def _get_total_cost(self, solution):
        """Calculates total cost for the solution."""
        pass

    def _modify(self, sol, trail):
        """Universal change of edges in the graph"""
        new_sol = {node: set(neighs) for node, neighs in sol.items()}
        for i in range(1, len(trail)):
            u, v = trail[i - 1], trail[i]
            if i % 2 == 1:  # Usuwanie
                new_sol[u].discard(v)
                new_sol[v].discard(u)
            else:  # Dodawanie
                new_sol[u].add(v)
                new_sol[v].add(u)
        return new_sol

    def _search(self, sol, trail, edges, current_total_gain):
        v_last = trail[-1]

        # Removing edges (Odd index in the trail)
        if len(trail) % 2 == 1:
            for v_next in sol[v_last]:
                edge = tuple(sorted((v_last, v_next)))
                if edge not in edges:
                    gain = self._get_gain(v_last, v_next, removing=True)
                    res = self._search(sol, trail + [v_next], edges | {edge}, current_total_gain + gain)
                    if res:
                        return res

        # Adding edges (Even index in the trail)
        else:
            for v_next in range(self.n):
                if v_next == v_last or v_next in sol[v_last]:
                    continue
                edge = tuple(sorted((v_last, v_next)))
                if edge not in edges:
                    gain = self._get_gain(v_last, v_next, removing=False)
                    if current_total_gain + gain > 0:  # Kryterium Zysku
                        if v_next == trail[0]:
                            potential = self._modify(sol, trail + [v_next])
                            if self._is_valid(potential):
                                return potential

                        if len(trail) < 2 * self.p:
                            res = self._search(sol, trail + [v_next], edges | {edge}, current_total_gain + gain)
                            if res:
                                return res
        return None

    def improve(self, initial_sol):
        """Loop improving initial solution."""
        self.best_solution = initial_sol
        improved = True
        while improved:
            improved = False
            for start_node in range(self.n):
                new_sol = self._search(self.best_solution, [start_node], set(), 0)
                if new_sol:
                    self.best_solution = new_sol
                    improved = True
                    break
        return self.best_solution

    def run(self):
        """Main loop that generates the solution and then improves it to find even better solution"""
        initial = self._generate_greedy()
        final = self.improve(initial)
        return final, self._get_total_cost(final)


class LinKerninghanForTSP(LinKernighan):
    def __init__(self, matrix, p=3):
        super().__init__(len(matrix), p)
        self.matrix = matrix

    def _get_gain(self, u, v, removing=True):
        # In TSP gain when removing edges is +distance, when adding it is -distance
        return self.matrix[u][v] if removing else -self.matrix[u][v]

    def _is_valid(self, potential_sol):
        # Checking if it is Hamiltonian cycle
        visited = {0}
        curr = 0
        for i in range(self.n):
            next_nodes = [v for v in potential_sol[curr] if v not in visited or (v == 0 and i == self.n - 1)]
            if not next_nodes:
                return False
            curr = next_nodes[0]
            visited.add(curr)
        return len(visited) == self.n

    def _generate_greedy(self):
        # Greedy algorithm to generate initial solution
        sol = {i: set() for i in range(self.n)}
        visited, curr = {0}, 0
        for _ in range(self.n - 1):
            next_node = min((v for v in range(self.n) if v not in visited), key=lambda v: self.matrix[curr][v])
            sol[curr].add(next_node)
            sol[next_node].add(curr)
            visited.add(next_node)
            curr = next_node
        sol[curr].add(0)
        sol[0].add(curr)
        return sol

    def _get_total_cost(self, solution):
        total_dist = 0
        for u in range(self.n):
            neighs = list(solution[u])
            total_dist += self.matrix[u][neighs[0]]
            total_dist += self.matrix[u][neighs[1]]

        # Divide by 2 because each edge was summed twice
        return total_dist / 2

    def _convert_solution(self, solution):
        # In Hamiltonian Cycle it does not matter which direction and starting
        # node we choose so we start with node 0
        path = [0]
        visited = {0}
        curr = 0

        # We traverse through n-1 edges to visit every city
        for _ in range(self.n - 1):
            # We look for neighbor of current vertex, which was not visited yet
            for neighbor in solution[curr]:
                if neighbor not in visited:
                    path.append(neighbor)
                    visited.add(neighbor)
                    curr = neighbor
                    break

        return path

    def run(self):
        solution, cost = super().run()
        return self._convert_solution(solution), cost


if __name__ == '__main__':
    # TASK 1 - test for TSP
    p = 3
    matrix = [[-1, 10, 1, 1], [10, -1, 1, 1], [1, 1, -1, 1], [1, 1, 1, -1]]
    solver = LinKerninghanForTSP(matrix, p)
    solution, cost = solver.run()
    print(f"Best solution found: {solution}")
    print(f"Cost of best solution: {cost}")
