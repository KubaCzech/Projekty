import random
from enum import Enum
from abc import ABC, abstractmethod


class SelectionMethods(Enum):
    Elitism = 'elitism'
    Tournament = 'tournament'
    Roulette = 'roulette'
    Random = 'random'


class GeneticAlgorithmBase(ABC):
    def __init__(
        self,
        pop_size=20,
        crossover_rate=0.9,
        mutation_rate=0.1,
        selection_method=SelectionMethods.Tournament,
        elitism=True,
    ):
        self.pop_size = pop_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.selection_method = selection_method
        self.elitism = elitism
        self.population = []
        self.best_solution = None

    @abstractmethod
    def fitness(self, solution):
        """
        Assess the solution (the higher fitness the better).

        Must be overriden in subclasses.

        Parameters
        ----------
        solution (list):
            Solution to be assessed

        Returns
        -------
        int:
            Value of fitness function
        """
        pass

    @abstractmethod
    def create_individual(self):
        """
        Creates new solution.
        """
        pass

    def create_initial_population(self):
        """
        Creates initial population by creating solutions one by one.
        """
        for _ in range(self.pop_size):
            solution = self.create_individual()
            self.population.append(solution)

    @abstractmethod
    def _crossover(self, p1, p2):
        """
        Abstract method to implement the specific crossover logic.

        Must be overridden in subclasses to define how two parents
        combine their genes for a specific problem (e.g., TSP or Set Partition).

        Parameters
        ----------
        p1 (list):
            First parent's chromosome.
        p2 (list):
            Second parent's chromosome.

        Returns
        -------
        list:
            The resulting offspring.
        """
        pass

    def crossover(self, p1, p2):
        """
        Decides whether to perform crossover based on the crossover_rate.

        This method acts as a wrapper for the abstract _crossover method.
        If the random roll exceeds the rate, it preserves the genetic
        material by returning the first parent.

        Parameters:
        ----------
        p1 (list):
            The genetic material of the first parent.
        p2 (list):
            The genetic material of the second parent.

        Returns:
        --------
        list:
            A new individual (child) or a copy of first parent.
        """
        if random.random() <= self.crossover_rate:
            return self._crossover(p1, p2)
        return p1

    @abstractmethod
    def _mutation(self, solution):
        """
        Abstract method to implement the specific mutation logic.

        Must be overridden in subclasses to define how mutation is
        performed for a specific problem (e.g., TSP or Set Partition).

        Parameters
        ----------
        solution (list):
            The genetic material of the solution.

        Returns
        -------
        list:
            The mutated solution.
        """
        pass

    def mutation(self, solution):
        """
        Decides whether to perform mutation based on the mutation_rate.

        This method acts as a wrapper for the abstract _mutation method.
        If the random roll exceeds the rate, it preserves the genetic
        material by returning the solution.

        Parameters:
        ----------
        solution (list):
            The genetic material of the solution.

        Returns:
        --------
        list:
            A new individual or a copy of solution.
        """
        if random.random() <= self.mutation_rate:
            return self._mutation(solution)
        return solution

    def _select_elitism(self):
        """
        Performs elitism selection (i. e. by choosing two solutions with
        highest fitness).
        """
        top_tier = max(1, int(self.pop_size * 0.25))
        return random.choice(self.population[:top_tier])

    def _select_tournament(self):
        """
        Performs tournament selection.
        """
        k = 3
        participants = random.sample(self.population, k)
        return max(participants, key=self.fitness)

    def _select_roulette(self):
        """
        Performs roulette selection.
        """
        min_fitness = min(self.fitness(ind) for ind in self.population)
        offset = abs(min_fitness) if min_fitness <= 0 else 0

        weights = [self.fitness(ind) + offset + 1e-6 for ind in self.population]
        return random.choices(self.population, weights=weights, k=1)[0]

    def _select_random(self):
        """
        Performs random selection.
        """
        return random.choice(self.population)

    def select(self):
        """
        Performs selection based on method chosen on the beggining.
        """
        return getattr(self, f"_select_{self.selection_method.value}")()

    def evolve(self):
        # 1. Sorting (highest to lowest)
        self.population.sort(key=self.fitness, reverse=True)

        # Update of best_solution
        current_best = self.population[0]
        if self.best_solution is None or self.fitness(current_best) > self.fitness(self.best_solution):
            self.best_solution = current_best[:]

        # 2. Creating new population
        new_pop = []

        # 3. Elitism
        if self.elitism:
            new_pop.append(self.best_solution[:])  # Najlepszy przechodzi dalej

        # 4. Creating offspring
        while len(new_pop) < self.pop_size:
            p1 = self.select()[:]
            p2 = self.select()[:]

            # Crossover and mutation
            child = self.crossover(p1, p2)
            child = self.mutation(child)
            new_pop.append(child)

        self.population = new_pop

    def run(self, generations=100):
        self.create_initial_population()

        for gen in range(generations):
            print(f"Generation number {gen+1}")
            self.evolve()

        final_solution = max(self.population, key=self.fitness)
        if self.fitness(final_solution) > self.fitness(self.best_solution):
            self.best_solution = final_solution[:]

        return self.best_solution

    def get_best_solution(self):
        return self.best_solution


# TASK 1 - SET PARTITION PROBLEM
class GeneticAlgorithmSetPartitionSolver(GeneticAlgorithmBase):
    def __init__(self, numbers, **kwargs):
        super().__init__(**kwargs)
        self.numbers = numbers
        self.n = len(numbers)

    def fitness(self, solution):
        sum_a = sum(self.numbers[i] for i in range(self.n) if solution[i] == 0)
        sum_b = sum(self.numbers[i] for i in range(self.n) if solution[i] == 1)

        return -abs(sum_a - sum_b)

    def create_individual(self):
        return [random.randint(0, 1) for _ in range(self.n)]

    def _crossover(self, p1, p2):
        point = random.randint(1, self.n - 1)
        child = p1[:point] + p2[point:]
        return child

    def _mutation(self, solution):
        idx = random.randint(0, self.n - 1)
        solution[idx] = 1 - solution[idx]
        return solution

    def run(self, **kwargs):
        best_solution = super().run(**kwargs)
        return self.fitness(best_solution) == 0


class GeneticAlgorithmTSPSolver(GeneticAlgorithmBase):
    def __init__(self, cities_matrix, **kwargs):
        super().__init__(**kwargs)

        self.cities = cities_matrix
        self.n = len(cities_matrix)

    def fitness(self, solution):
        total = sum(self.cities[solution[i]][solution[i + 1]] for i in range(self.n - 1))
        total += self.cities[solution[-1]][solution[0]]
        return -total

    def create_individual(self):
        solution = list(range(self.n))
        random.shuffle(solution)
        return solution

    def _crossover(self, p1, p2):
        start, end = sorted(random.sample(range(self.n), 2))
        middle_fragment = p1[start : end + 1]

        # Fill the missing places with cities from p2 that are not already in use
        p2_filtered = [city for city in p2 if city not in middle_fragment]
        return p2_filtered[:start] + middle_fragment + p2_filtered[start:]

    def _mutation(self, solution):
        idx1, idx2 = tuple(random.sample(range(self.n - 1), 2))
        solution[idx1], solution[idx2] = solution[idx2], solution[idx1]
        return solution

    def run(self, **kwargs):
        best_solution = super().run(**kwargs)
        return abs(self.fitness(best_solution))


numbers = [1, 2, 3, 4, 10]
solver = GeneticAlgorithmSetPartitionSolver(numbers=numbers)
print(f"Set {numbers} can be partitioned into two subsets: {solver.run()}")  # True

# TASK 2 - TESTING DIFFERENT SELECTION MECHANISMS
# Random
solver = GeneticAlgorithmSetPartitionSolver(selection_method=SelectionMethods.Random, numbers=numbers)
print(f"Set {numbers} can be partitioned into two subsets: {solver.run()}")

# Roulette
solver = GeneticAlgorithmSetPartitionSolver(selection_method=SelectionMethods.Roulette, numbers=numbers)
print(f"Set {numbers} can be partitioned into two subsets: {solver.run()}")

# Elitism
solver = GeneticAlgorithmSetPartitionSolver(selection_method=SelectionMethods.Elitism, numbers=numbers)
print(f"Set {numbers} can be partitioned into two subsets: {solver.run()}")

# TASK 3 - TSP
cities = [
    [0, 10, 20, 22.36, 14.14, 10],
    [10, 0, 10, 14.14, 10, 14.14],
    [20, 10, 0, 10, 14.14, 22.36],
    [22.36, 14.14, 10, 0, 10, 20],
    [14.14, 10, 14.14, 10, 0, 10],
    [10, 14.14, 22.36, 20, 10, 0],
]
solver = GeneticAlgorithmTSPSolver(cities_matrix=cities)
print(f"Minimal length of path found: {solver.run()}")  # Optimal = 60
