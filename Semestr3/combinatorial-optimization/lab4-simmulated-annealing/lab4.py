# l = []
# for i in range(10):
#     solution = simulated_annealing(1000, 0.99, generate_random(), 0.01, -2, 4)
#     print(round(solution, 2), round(function(solution), 4))
#     l.append((solution, function(solution)))
# l.sort(key=lambda x: x[1])
# print("Best solution is for ", round(l[0][0], 2), " and equals to ", round(l[0][1], 4))

import math
import random
import numpy as np
from abc import ABC, abstractmethod


class SimulatedAnnealing(ABC):
    def __init__(self, initial_t=100.0, cooling_rate=0.99, eps=1e-6):
        self.t = initial_t
        self.cooling_rate = cooling_rate
        self.eps = eps
        self.best_solution = None
        self.best_energy = float('inf')

    @abstractmethod
    def get_initial_state(self):
        pass

    @abstractmethod
    def get_neighbor(self, current_state):
        pass

    @abstractmethod
    def get_energy(self, state):
        pass

    def run(self):
        current_state = self.get_initial_state()
        current_energy = self.get_energy(current_state)

        change = True

        self.best_solution = current_state
        self.best_energy = current_energy

        while round(self.t, 4) > 0 or change:
            neighbor = self.get_neighbor(current_state)
            neighbor_energy = self.get_energy(neighbor)

            change = False

            # Acceptance probability logic
            if neighbor_energy < current_energy:
                accept = True
            else:
                p = np.exp((current_energy - neighbor_energy) / (self.t + self.eps))
                accept = np.random.rand() < p

            if accept:
                current_state = neighbor
                current_energy = neighbor_energy

                if current_energy < self.best_energy:
                    self.best_energy = current_energy
                    self.best_solution = current_state
                change = True

            self.t *= self.cooling_rate

        return self.best_solution, self.best_energy


class SimulatedAnnealingForPolynomialFunction(SimulatedAnnealing):
    def __init__(self, domain: tuple[int, int], eval_function, step: float = 1e-2, **kwargs):
        super().__init__(**kwargs)
        self.lower_limit, self.upper_limit = domain
        self.step = step
        self.evaluation_function = eval_function

    def get_energy(self, state):
        return self.evaluation_function(state)

    def get_neighbor(self, current_state):
        if random.random() > 0.5:
            return np.clip(current_state - self.step, self.lower_limit, self.upper_limit)
        return np.clip(current_state + self.step, self.lower_limit, self.upper_limit)

    def get_initial_state(self):
        return random.uniform(self.lower_limit, self.upper_limit)


class SimulatedAnnealingForTSP(SimulatedAnnealing):
    def __init__(self, cities, **kwargs):
        super().__init__(**kwargs)
        self.cities = cities
        self.n = len(cities)

    def get_energy(self, state):
        return sum(self.cities[state[i]][state[i + 1]] for i in range(self.n - 1)) + self.cities[state[-1]][state[0]]

    def get_neighbor(self, current_state):
        new_state = current_state[:]
        idx0, idx1 = tuple(random.sample(list(range(self.n)), 2))
        new_state[idx0], new_state[idx1] = new_state[idx1], new_state[idx0]
        return new_state

    def get_initial_state(self):
        solution = list(range(self.n))
        random.shuffle(solution)
        return solution


class SimulatedAnnealingForMinimumVertexCover(SimulatedAnnealing):
    def __init__(self, adj_matrix, penalty=10, **kwargs):
        super().__init__(**kwargs)
        self.adj_matrix = adj_matrix
        self.n = len(adj_matrix)
        self.penalty = penalty

    def get_energy(self, state):
        size = np.sum(state)
        uncovered_edges = sum(
            [
                1
                for i in range(self.n)
                for j in range(i + 1, self.n)
                if self.adj_matrix[i][j] == 1 and state[i] == 0 and state[j] == 0
            ]
        )
        return size + (uncovered_edges * self.penalty)

    def get_neighbor(self, current_state):
        new_state = current_state[:]
        idx = random.randrange(self.n)
        new_state[idx] = 1 - new_state[idx]
        return new_state

    def get_initial_state(self):
        return [random.randint(0, 1) for _ in range(self.n)]


def get_petersen_graph():
    adj = np.zeros((10, 10), dtype=int)

    # External ring: 0-1, 1-2, 2-3, 3-4, 4-0
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]

    # Internal star: 5-7, 7-9, 9-6, 6-8, 8-5
    edges += [(5, 7), (7, 9), (9, 6), (6, 8), (8, 5)]

    # Connections between ring and star: 0-5, 1-6, 2-7, 3-8, 4-9
    edges += [(0, 5), (1, 6), (2, 7), (3, 8), (4, 9)]

    for u, v in edges:
        adj[u][v] = 1
        adj[v][u] = 1
    return adj


if __name__ == '__main__':
    # TASK 1 - Minimum of Polynomial Function using Simmulated Annealing
    def function(x):
        return x**6 - 7 * x**5 + 7 * x**4 + 35 * x**3 - 56 * x**2 - 28 * x + 48

    solver = SimulatedAnnealingForPolynomialFunction((-2, 4), function)
    solution, energy = solver.run()
    print(f"Solution: {solution}")  # Should be approx. -1.62; however possible options are: 1.46, 3.66
    print(f"Energy: {energy}")

    # TASK 2 - TSP using Simulated Annealing
    cities = [
        [0, 10, 20, 22.36, 14.14, 10],
        [10, 0, 10, 14.14, 10, 14.14],
        [20, 10, 0, 10, 14.14, 22.36],
        [22.36, 14.14, 10, 0, 10, 20],
        [14.14, 10, 14.14, 10, 0, 10],
        [10, 14.14, 22.36, 20, 10, 0],
    ]
    solver = SimulatedAnnealingForTSP(cities)
    solution, energy = solver.run()
    print(f"Solution: {solution}")
    print(f"Energy: {energy}")  # Should be 60

    # TASK 3 - Minimum Vertex Cover using Simulated Annealing
    adj_matrix = get_petersen_graph()
    solver = SimulatedAnnealingForMinimumVertexCover(adj_matrix)
    solution, energy = solver.run()
    print(f"Solution: {solution}")
    print(f"Energy: {energy}")  # Should be 6
