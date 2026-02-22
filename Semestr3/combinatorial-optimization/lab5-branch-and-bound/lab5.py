from abc import ABC, abstractmethod
import heapq


# Nodes definition
class AssignmentNode:
    def __init__(self, level, value, solution):
        self.level = level
        self.value = value
        self.path = solution  # List of indices of chosen tasks

    # heapq needs comparison of nodes for the same priority
    def __lt__(self, other):
        return self.level > other.level


class KnapsackNode:
    def __init__(self, level, value, weight, path):
        self.level = level
        self.value = value
        self.weight = weight
        self.path = path  # List of indices of chosen items

    # heapq needs comparison of nodes for the same priority
    def __lt__(self, other):
        return self.level > other.level


class TSPNode:
    def __init__(self, level, value, path):
        self.level = level  # Number of visited cities
        self.value = value  # Cost of actual path
        self.path = path  # Order of the cities

    def __lt__(self, other):
        return self.level > other.level


# Branch and Bound template
class BranchAndBound(ABC):
    def __init__(self, is_minimization=True):
        self.is_minimization = is_minimization
        self.best_solution = None
        self.best_value = float('inf') if is_minimization else float('-inf')

    @abstractmethod
    def get_initial_node(self):
        """Returns initial node"""
        pass

    @abstractmethod
    def calculate_bound(self, node):
        """Calculates bounds (Lower Bound for min, Upper Bound for max)."""
        pass

    @abstractmethod
    def get_children(self, node):
        """Generates possible branches."""
        pass

    @abstractmethod
    def is_complete(self, node):
        """Checks if node represents complete solution."""
        pass

    def run(self):
        # Queue stores: (priority, node)
        start_node = self.get_initial_node()
        initial_bound = self.calculate_bound(start_node)

        priority = initial_bound if self.is_minimization else -initial_bound
        pq = [(priority, start_node)]

        while pq:
            current_bound_prio, node = heapq.heappop(pq)
            current_bound = current_bound_prio if self.is_minimization else -current_bound_prio

            # Pruning: if constraint is worse than our record, reject the branch
            if self.is_minimization:
                if current_bound >= self.best_value:
                    continue
            else:
                if current_bound <= self.best_value:
                    continue

            if self.is_complete(node):
                if (self.is_minimization and node.value < self.best_value) or (
                    not self.is_minimization and node.value > self.best_value
                ):
                    self.best_value = node.value
                    self.best_solution = node.path
                continue

            # Branching
            for child in self.get_children(node):
                child_bound = self.calculate_bound(child)

                # We add to the queue only if it prospers
                if self.is_minimization:
                    if child_bound < self.best_value:
                        heapq.heappush(pq, (child_bound, child))
                else:
                    if child_bound > self.best_value:
                        heapq.heappush(pq, (-child_bound, child))

        return self.best_solution, self.best_value


# Implementation of Branch and Bound for specific problems
class BranchAndBoundAssignmentProblem(BranchAndBound):
    def __init__(self, costs):
        # costs is a square matrix: costs[worker][task]
        super().__init__(is_minimization=True)
        self.costs = costs
        self.n = len(self.costs)

    def get_initial_node(self):
        return AssignmentNode(level=0, value=0, solution=[])

    def calculate_bound(self, node):
        """
        Lower Bound = Current Value + Minimum possible cost for remaining workers.
        """
        bound = node.value
        assigned_tasks = set(node.path)

        # Iterating over all workers without a task
        for worker_idx in range(node.level, self.n):
            min_val = float('inf')
            for task_idx in range(self.n):
                # Looking for cheapest unassigned task
                if task_idx not in assigned_tasks:
                    if self.costs[worker_idx][task_idx] < min_val:
                        min_val = self.costs[worker_idx][task_idx]

            if min_val != float('inf'):
                bound += min_val
        return bound

    def get_children(self, node):
        children = []
        worker_idx = node.level  # Current worker to assign
        assigned_tasks = set(node.path)

        for task_idx in range(self.n):
            if task_idx not in assigned_tasks:
                new_value = node.value + self.costs[worker_idx][task_idx]
                new_path = node.path + [task_idx]

                children.append(AssignmentNode(level=node.level + 1, value=new_value, solution=new_path))
        return children

    def is_complete(self, node):
        return node.level == self.n


class BranchAndBoundKnapsackProblem(BranchAndBound):
    def __init__(self, capacity, values, weights):
        super().__init__(is_minimization=False)
        self.capacity = capacity

        # Store items as (value, weight, original_index)
        # and sort by efficiency (value/weight) descending.
        self.items = sorted(
            [(values[i], weights[i], i) for i in range(len(values))], key=lambda x: x[0] / x[1], reverse=True
        )
        self.n = len(self.items)

    def get_initial_node(self):
        return KnapsackNode(level=0, value=0, weight=0, path=[])

    def calculate_bound(self, node):
        """Calculates Upper Bound using linear relaxation method"""
        if node.weight > self.capacity:
            return -1

        v_bound = node.value
        total_w = node.weight
        j = node.level

        # Greedily add whole items to the bound calculation.
        while j < self.n and total_w + self.items[j][1] <= self.capacity:
            total_w += self.items[j][1]
            v_bound += self.items[j][0]
            j += 1

        # Add the fractional part of the next item to get a tight upper bound.
        # It is not possible to produce better solution so it is maximum
        if j < self.n:
            v_bound += (self.capacity - total_w) * (self.items[j][0] / self.items[j][1])

        return v_bound

    def get_children(self, node):
        children = []
        # Safety check to prevent IndexOutOfBounds.
        if node.level >= self.n:
            return children

        v, w, idx = self.items[node.level]

        # Option 1: we choose an item if it fits
        if node.weight + w <= self.capacity:
            children.append(
                KnapsackNode(
                    node.level + 1,
                    node.value + v,
                    node.weight + w,
                    node.path + [idx],  # Store the original index for the result
                )
            )

        # Option 2: item doesn't fit or we choose not to take it
        # This branch is essential for exploring the "exclude" scenario.
        children.append(KnapsackNode(node.level + 1, node.value, node.weight, node.path))
        return children

    def is_complete(self, node):
        return node.level == self.n


class BrancAndBoundTSP(BranchAndBound):
    def __init__(self, matrix):
        super().__init__(is_minimization=True)
        self.matrix = matrix
        self.n = len(matrix)

    def get_initial_node(self):
        return TSPNode(level=1, value=0, path=[0])

    def calculate_bound(self, node):
        """
        Simplified lowe bound:
        Actual cost + sum of minimal edges outgoing for all remaining cities.
        """
        if node.level == self.n:
            return node.value

        bound = node.value
        visited = set(node.path)
        last_city = node.path[-1]

        # 1. Cost of exiting penultimate city (last unordered or return to 0)
        min_out = float('inf')
        for j in range(self.n):
            if j not in visited or (j == 0 and len(visited) == self.n):
                if self.matrix[last_city][j] != -1:  # -1 = records lying on the diagonal (entering city A from A)
                    min_out = min(min_out, self.matrix[last_city][j])

        if min_out != float('inf'):
            bound += min_out

        # 2. Cost of visiting unvisited city
        for i in range(1, self.n):
            if i not in visited:
                min_in = float('inf')
                for j in range(self.n):
                    if i != j and self.matrix[j][i] != -1:
                        min_in = min(min_in, self.matrix[j][i])
                if min_in != float('inf'):
                    bound += min_in

        return bound

    def get_children(self, node):
        children = []
        last_city = node.path[-1]
        visited = set(node.path)

        for next_city in range(self.n):
            if next_city not in visited and self.matrix[last_city][next_city] != -1:
                new_value = node.value + self.matrix[last_city][next_city]

                # If it is penultimate city, add cost of returning to the first city
                if len(node.path) == self.n - 1:
                    return_cost = self.matrix[next_city][0]
                    if return_cost != -1:
                        children.append(
                            TSPNode(level=node.level + 1, value=new_value + return_cost, path=node.path + [next_city])
                        )
                else:
                    children.append(TSPNode(level=node.level + 1, value=new_value, path=node.path + [next_city]))
        return children

    def is_complete(self, node):
        return node.level == self.n


if __name__ == '__main__':
    # TASK 1 - Assignment Problem using Branch and Bound
    costs = [[9, 2, 7, 8], [6, 4, 3, 7], [5, 8, 1, 8], [7, 6, 9, 4]]

    solver = BranchAndBoundAssignmentProblem(costs)
    solution, value = solver.run()

    print(f"Solution found: {solution}")
    print(f"Best value found: {value}", end='\n\n')  # 13

    # TASK 2 - Knapsack Problem using Branch and Bound
    capacity = 9
    weights = [3, 2, 4, 5, 1]
    values = [50, 40, 70, 80, 10]
    solver = BranchAndBoundKnapsackProblem(capacity, values, weights)
    solution, value = solver.run()
    print(f"Solution found: {solution}")
    print(f"Best value found: {value}", end='\n\n')  # 160

    capacity = 50
    weights = [10, 20, 30]
    values = [60, 100, 120]
    solver = BranchAndBoundKnapsackProblem(capacity, values, weights)
    solution, value = solver.run()
    print(f"Solution found: {solution}")
    print(f"Best value found: {value}", end='\n\n')  # 220

    # TASK 3 - TSP using Branch and Bound
    cities = [[-1, 10, 15, 20], [10, -1, 35, 25], [15, 35, -1, 30], [20, 25, 30, -1]]

    solver = BrancAndBoundTSP(cities)
    best_solution, best_value = solver.run()

    print(f"Najlepsza trasa: {best_solution}")
    print(f"Minimalny koszt: {best_value}")  # 80
