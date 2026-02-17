import random
from time import time


def random_array(N, min=1, max=100):
    return [random.randint(min, max) for _ in range(N)]


def conduct_experiments(sorting_algorithm, list_to_sort):
    start_time = time()
    sorted_list = sorting_algorithm(list_to_sort)
    end_time = time()

    assert sorted_list == sorted(list_to_sort), "Sorting algorithm did not sort the list correctly."

    return end_time - start_time
