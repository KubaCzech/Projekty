import sys

# n = number of things
# c = size of the knapsack


def read_data():
    try:
        input_data = sys.stdin.read().split()
        if not input_data:
            return

        n = int(input_data[0])
        capacity = int(input_data[1])

        items = []
        idx = 2
        for _ in range(n):
            v = int(input_data[idx])
            s = int(input_data[idx + 1])
            items.append((v, s))
            idx += 2

    except EOFError:
        pass

    return n, capacity, items


def solve_knapsack(n, capacity, items):
    # dp[i][j] is maximal value, we can achieve for first i items and size j
    # To achieve that, we create matrix (n+1) x (capacity+1) filled with 0
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        value, size = items[i - 1]
        for j in range(capacity + 1):
            if size <= j:
                dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - size] + value)
            else:  # item doesn't fit
                dp[i][j] = dp[i - 1][j]

    return dp[n][capacity], dp


def solve_set_partition(numbers: list[int]) -> bool:
    """
    Solve the decision version of the Set Partition Problem.

    This implementation reduces the Set Partition Problem to a 0/1 Knapsack
    instance. It checks if the input array can be split into two subsets
    with an equal sum of elements.

    Parameters
    ----------
    numbers : list of int
        A list of positive integers to be partitioned.

    Returns
    -------
    bool
        True if an equal partition exists, False otherwise.

    Notes
    -----
    The reduction follows these steps:
    1. Verify if the total sum :math:`S` is even.
    2. Set the target capacity :math:`C = S / 2`.
    3. Treat each number as an item where weight equals value.
    4. Solve for the maximum value achievable with capacity :math:`C`.
    """
    total_sum = sum(numbers)

    # Sum must be even
    if total_sum % 2 != 0:
        print('lol')
        return False

    target = total_sum // 2
    n = len(numbers)

    # Mapping Set Partition Problem to Knapsack Problem; each number is an item, where value = size
    items = [(num, num) for num in numbers]

    # Reusing previously implemented Knapsack Problem
    max_value = solve_knapsack(n, target, items)[0]

    return max_value == target


if __name__ == '__main__':
    # TASK 1 - Knapsack Problem using Pseudopolynomial Algorithm
    n, capacity, items = read_data()
    print("Maximal value of knapsack:", solve_knapsack(n, capacity, items)[0])

    # TASK 2 - Set Partition using Pseudopolynomial Algorithm
    numbers = [1, 2, 3, 4, 5, 5]
    print(f"Set Partition of {[1, 2, 3, 4, 5, 5]} possible: {solve_set_partition(numbers)}")
