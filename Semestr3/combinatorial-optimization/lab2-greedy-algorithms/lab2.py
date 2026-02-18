import math


def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def solve_tsp_nearest_neighbor(cities):
    """
    Greedy approach to TSP: Always pick the closest unvisited vertex.

    Notes
    -----
    Nearest Neighbor strategy fails when a short-term gain forces a massive long-term cost.
    """
    unvisited = list(range(len(cities)))
    current_city = unvisited.pop(0)  # Start at the first city
    tour = [current_city]
    total_dist = 0

    while unvisited:
        # Find the nearest unvisited city
        next_city = min(unvisited, key=lambda city: distance(cities[current_city], cities[city]))
        total_dist += distance(cities[current_city], cities[next_city])
        current_city = next_city
        unvisited.remove(next_city)
        tour.append(next_city)

    # Return to start
    total_dist += distance(cities[current_city], cities[tour[0]])
    return tour, total_dist


def greedy_knapsack(capacity, items):
    """
    Greedy approach for Knapsack: Always pick the item with highest
    value/weight (balancing between value and weight simultanously)

    Notes
    -----
    The greedy approach fails for the 0/1 Knapsack because it cannot
    "look ahead" to see if a slightly less dense item would fill the
    bag more efficiently.
    """
    # Sort by value/weight ratio
    items.sort(key=lambda x: x[0] / x[1], reverse=True)

    total_value = 0
    for value, weight in items:
        if capacity >= weight:
            capacity -= weight
            total_value += value
    return total_value


def solve_activity_selection(activities):
    """
    Sort by finish time and pick non-overlapping activities.
    """
    # Sort activities by their end time (second element of tuple)
    sorted_activities = sorted(activities, key=lambda x: x[1])

    selected = []
    if not sorted_activities:
        return selected

    # Pick the first activity (ends earliest)
    last_end_time = sorted_activities[0][1]
    selected.append(sorted_activities[0])

    for i in range(1, len(sorted_activities)):
        start, end = sorted_activities[i]
        # If it starts after or when the previous one ends, pick it
        if start >= last_end_time:
            selected.append((start, end))
            last_end_time = end

    return selected


if __name__ == '__main__':
    # TASK 1 - TSP using Greedy Algorithm
    cities = [(0, 0), (1, 0), (10, 0), (11, 0)]
    print(solve_tsp_nearest_neighbor(cities))

    # TASK 2 - Knapsack Problem using Greedy Algorithm
    items = [(50, 3), (40, 2), (70, 4), (80, 5), (10, 1)]
    print(greedy_knapsack(6, items))

    # TASK 3 - Activities Selection Problem using Greedy Algorithm
    activities = [(12, 13), (12, 15), (13, 14), (14, 16)]
    print(f"Activities selected: {solve_activity_selection(activities)}")
