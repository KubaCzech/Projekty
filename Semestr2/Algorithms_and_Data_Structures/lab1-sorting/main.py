from utils import random_array, conduct_experiments
from sorting_algorithms import *


if __name__ == "__main__":
    mini = 0
    maxi = 100000
    n = 1000

    times = {}

    list_to_sort = random_array(n, mini, maxi)
    for algorithm in [
        selection_sort,
        insertion_sort,
        bubble_sort,
        quick_sort,
        merge_sort,
        shell_sort,
        heap_sort,
        counting_sort,
    ]:
        time_taken = conduct_experiments(algorithm, list_to_sort.copy())
        times[algorithm.__name__] = time_taken

    results = times.items()
    sorted_results = sorted(results, key=lambda x: x[1])
    print()
    print("Sorting algorithms ranked by time taken:")
    for name, time_taken in sorted_results:
        print(f"{name}: {time_taken:.6f} seconds")
    print()
