import numpy as np
from pulp import *
import matplotlib.pyplot as plt

### distance matrix
D = [
    [16.160, 24.080, 24.320, 21.120],
    [19.000, 26.470, 27.240, 17.330],
    [25.290, 32.490, 33.420, 12.250],
    [0.000, 7.930, 8.310, 36.120],
    [3.070, 6.440, 7.560, 37.360],
    [1.220, 7.510, 8.190, 36.290],
    [2.800, 10.310, 10.950, 33.500],
    [2.870, 5.070, 5.670, 38.800],
    [3.800, 8.010, 7.410, 38.160],
    [12.350, 4.520, 4.350, 48.270],
    [11.110, 3.480, 2.970, 47.140],
    [21.990, 22.020, 24.070, 39.860],
    [8.820, 3.300, 5.360, 43.310],
    [7.930, 0.000, 2.070, 43.750],
    [9.340, 2.250, 1.110, 45.430],
    [8.310, 2.070, 0.000, 44.430],
    [7.310, 2.440, 1.110, 43.430],
    [7.550, 0.750, 1.530, 43.520],
    [11.130, 18.410, 19.260, 25.400],
    [17.490, 23.440, 24.760, 23.210],
    [11.030, 18.930, 19.280, 25.430],
    [36.120, 43.750, 44.430, 0.000]
]

### labor intensity
P = [0.1609, 0.1164, 0.1026, 0.1516, 0.0939, 0.1320, 0.0687, 0.0930, 0.2116, 0.2529, 0.0868, 0.0828, 0.0975, 0.8177,
     0.4115, 0.3795, 0.0710, 0.0427, 0.1043, 0.0997, 0.1698, 0.2531]

### current assignment
A = [
    [0, 0, 0, 1],
    [0, 0, 0, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 0],
    [1, 0, 0, 0],
    [1, 0, 0, 0],
    [1, 0, 0, 0],
    [1, 0, 0, 0],
    [0, 0, 1, 0],
    [0, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 0, 0],
    [1, 0, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1],
    [0, 0, 0, 1],
    [0, 0, 0, 1],
    [0, 0, 0, 1],
]

### current locations of representatives
L = [4, 14, 16, 22]

def solve_epsilon_constraint(epsilon):
    num_regions = len(D)
    num_reps = len(D[0])
    current_assignment = np.argmax(np.array(A), axis=1)

    # Create LP problem
    prob = pulp.LpProblem("Epsilon_Constraint", sense = LpMinimize)

    # Decision variables
    x = [[pulp.LpVariable(f"x_{i}_{j}", cat='Binary') for j in range(num_reps)] for i in range(num_regions)]

    # Objective: Minimize total distance
    prob += pulp.lpSum(D[i][j] * x[i][j] for i in range(num_regions) for j in range(num_reps))

    # Constraint 1: Each region assigned to one rep
    for i in range(num_regions):
        prob += pulp.lpSum(x[i][j] for j in range(num_reps)) == 1

    # Constraint 2: Rep labor intensity in [0.9, 1.1]
    for j in range(num_reps):
        prob += pulp.lpSum(P[i] * x[i][j] for i in range(num_regions)) >= 0.9
        prob += pulp.lpSum(P[i] * x[i][j] for i in range(num_regions)) <= 1.1

    # Constraint 3: f2 <= epsilon
    # Change penalty: 1 if current rep ≠ new rep (weighted by labor)
    change_cost = pulp.lpSum(
        P[i] * (1 - x[i][current_assignment[i]]) for i in range(num_regions)
    )

    prob += change_cost * 100 <= epsilon
    status = prob.solve()
    # return LpStatus[prob.status]

    if LpStatus[prob.status] == "Optimal":
        assignment = np.array([[x[i][j].varValue for j in range(num_reps)] for i in range(num_regions)])
        total_distance = pulp.value(prob.objective)
        change_percent = pulp.value(change_cost) * 100
        return assignment, total_distance, change_percent
    else:
        return None, None, None

# interval = 1
results = set()
for eps in np.linspace(1, 401, 1000):
    assigment, total_distance, change_percent = solve_epsilon_constraint(eps)
    if total_distance is not None and change_percent is not None and assigment is not None:
        results.add((np.round(total_distance, 2), np.round(change_percent, 2)))

results = list(results)
results.sort(key = lambda x: x[0])
results = results[:10]
print(results)

plt.scatter([i[0] for i in results], [i[1] for i in results])
plt.xlabel('Total distance [f1]')
plt.ylabel('Total value of change [f2]')
plt.title('Pareto optimal solutions')
plt.show()