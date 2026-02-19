import numpy as np
import random as rnd

from math import sin
from abc import ABC, abstractmethod


# w = 0.95
# cl = 0.02
# cg = 0.03


class ParticleSwarmOptimizationBase(ABC):
    def __init__(self, num_particles, dimensions, w=0.5, cg=1.5, cp=1.5):
        self.num_particles = num_particles
        self.dimensions = dimensions

        # Hyperparameters (Inertia, Global, Personal)
        self.w, self.cg, self.cp = w, cg, cp

        # These will be initialized in the children
        self.pos = None
        self.vel = None

        # Memory tracking
        self.p_best_pos = None
        self.p_best_val = None
        self.best_solution = None  # Polish: Nasze optymalne rozwiązanie
        self.best_value = float('inf')

    @abstractmethod
    def _calculate_fitness(self, position):
        """
        Objective function to minimize.
        """
        pass

    @abstractmethod
    def _update_position(self):
        """
        Logic for moving particles (Continuous vs Discrete).
        """
        pass

    def _update_bests(self):
        """
        Standard logic to update personal and global records.
        """
        for i in range(self.num_particles):
            current_val = self._calculate_fitness(self.pos[i])
            if current_val < self.p_best_val[i]:
                self.p_best_val[i] = current_val
                self.p_best_pos[i] = np.copy(self.pos[i])

                if current_val < self.best_value:
                    self.best_value = current_val
                    self.best_solution = np.copy(self.pos[i])

    def run(self, iterations=100):
        # Initial evaluation
        self._update_bests()

        for _ in range(iterations):
            rg = np.random.rand(self.num_particles, self.dimensions)
            rp = np.random.rand(self.num_particles, self.dimensions)

            # Update velocity using the standard PSO formula
            self.vel = (
                self.w * self.vel
                + self.cg * rg * (self.best_solution - self.pos)
                + self.cp * rp * (self.p_best_pos - self.pos)
            )

            # Move particles (different for each child)
            self._update_position()

            # Refresh records
            self._update_bests()

        return self.best_solution, self.best_value


class ParticleSwarmOptimizationForContinousFunction(ParticleSwarmOptimizationBase):
    def __init__(self, func, bounds, num_particles=30, **kwargs):
        dims = len(bounds)
        super().__init__(num_particles, dims, **kwargs)
        self.func = func
        self.bounds = np.array(bounds)

        # Continuous initialization
        self.pos = np.random.uniform(self.bounds[:, 0], self.bounds[:, 1], (num_particles, dims))
        self.vel = np.random.uniform(-1, 1, (num_particles, dims))
        self.p_best_pos = np.copy(self.pos)
        self.p_best_val = np.full(num_particles, float('inf'))

    def _calculate_fitness(self, p):
        return self.func(p[0], p[1])

    def _update_position(self):
        # Standard addition for continuous space
        self.pos += self.vel
        self.pos = np.clip(self.pos, self.bounds[:, 0], self.bounds[:, 1])


class ParticleSwarmOptimizationForSetPartition(ParticleSwarmOptimizationBase):
    def __init__(self, numbers, num_particles=20, **kwargs):
        dims = len(numbers)
        super().__init__(num_particles, dims, **kwargs)
        self.numbers = np.array(numbers)

        # Discrete initialization (binary vectors)
        self.pos = np.random.randint(2, size=(num_particles, dims))
        self.vel = np.random.uniform(-4, 4, (num_particles, dims))
        self.p_best_pos = np.copy(self.pos)
        self.p_best_val = np.full(num_particles, float('inf'))

    def _calculate_fitness(self, bitmask):
        sum1 = np.sum(self.numbers[bitmask == 1])
        sum2 = np.sum(self.numbers[bitmask == 0])
        return abs(sum1 - sum2)

    def _update_position(self):
        # Probability-based update for binary space
        # Sigmoid converts velocity for probability of occurring 1
        probs = 1 / (1 + np.exp(-self.vel))
        self.pos = (np.random.rand(self.num_particles, self.dimensions) < probs).astype(int)


if __name__ == '__main__':
    # TASK 1 - Minimum of a continous function using PSO
    def f(x, y):
        return sin(x) ** 2 + sin(y) ** 2 + sin(x) * sin(y)

    solver = ParticleSwarmOptimizationForContinousFunction(f, [(-3, 3), (-3, 3)])
    solution, value = solver.run()
    print(f"Best solution found: {solution}")
    print(f"Value of the best solution: {value}")

    # TASK 2 - Set Partition Problem using PSO
    # numbers = [4, 5, 6, 7, 8, 10, 12, 18]
    numbers = [771, 121, 281, 854, 885, 734, 486, 1003, 83, 62]  # Karmakar-Karp challenge
    solver = ParticleSwarmOptimizationForSetPartition(numbers, num_particles=40)
    solution, value = solver.run()
    print(f"Best solution found: {solution}")
    print(f"Value of the best solution: {value}")
