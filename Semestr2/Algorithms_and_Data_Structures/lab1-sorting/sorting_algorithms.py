import random


# Selection sort
def selection_sort(list_to_sort: list) -> list:
    """
    Sort the input list using the selection sort algorithm.

    Parameters:
    -----------
    list_to_sort (list):
        The list of elements to be sorted.

    Returns:
    --------
    list:
        The sorted list.

    Notes:
    ------
    1. Time complexity:
    - Pesimistic case: O(n^2)
    - Average case: O(n^2)
    - Optimistic case: O(n^2)
    2. Space complexity: O(1)
    3. Stability: Not stable
    4. In-place: Yes
    """
    for i in range(len(list_to_sort)):
        min_idx = i
        for j in range(i + 1, len(list_to_sort)):
            if list_to_sort[j] < list_to_sort[min_idx]:
                min_idx = j
        list_to_sort[i], list_to_sort[min_idx] = list_to_sort[min_idx], list_to_sort[i]
    return list_to_sort


# Insertion sort
def insertion_sort(list_to_sort):
    """
    Sort the input list using the insertion sort algorithm.

    Parameters:
    -----------
    list_to_sort (list):
        The list of elements to be sorted.

    Returns:
    --------
    list:
        The sorted list.

    Notes:
    ------
    1. Time complexity:
    - Pesimistic case: O(n^2)
    - Average case: O(n^2)
    - Optimistic case: O(n) (when the list is already sorted)
    2. Space complexity: O(1)
    3. Stability: Stable
    4. In-place: Yes
    Very fast when array is almost sorted.
    """
    for i in range(1, len(list_to_sort)):
        to_insert = list_to_sort[i]
        j = i - 1

        while j >= 0 and list_to_sort[j] > to_insert:
            list_to_sort[j + 1] = list_to_sort[j]
            j -= 1
        list_to_sort[j + 1] = to_insert
    return list_to_sort


# Bubble sort
def bubble_sort(list_to_sort):
    """
    Sort the input list using the bubble sort algorithm.

    Parameters:
    -----------
    list_to_sort (list):
        The list of elements to be sorted.

    Returns:
    --------
    list:
        The sorted list.

    Notes:
    ------
    1. Time complexity:
    - Pesimistic case: O(n^2)
    - Average case: O(n^2)
    - Optimistic case: O(n) (when the list is already sorted and algorithm is properly optimized)
    2. Space complexity: O(1)
    3. Stability: Stable
    4. In-place: Yes
    """
    for i in range(len(list_to_sort)):
        for j in range(0, len(list_to_sort) - i - 1):
            if list_to_sort[j] > list_to_sort[j + 1]:
                list_to_sort[j], list_to_sort[j + 1] = list_to_sort[j + 1], list_to_sort[j]
    return list_to_sort


# Quick sort
def quick_sort(list_to_sort):
    """
    Sort the input list using the quick sort algorithm.

    Parameters:
    -----------
    list_to_sort (list):
        The list of elements to be sorted.

    Returns:
    --------
    list:
        The sorted list.

    Notes:
    ------
    1. Time complexity:
    - Pesimistic case: O(n^2) (when the smallest or largest element is always chosen as the pivot)
    - Average case: O(n log n)
    - Optimistic case: O(n log n) (when the pivot divides the list into two equal halves)
    2. Space complexity: O(log n) on average (due to recursive stack space), O(n) in the worst case
    3. Stability: Not stable
    4. In-place: Yes (if implemented with in-place partitioning)
    """
    if len(list_to_sort) <= 1:
        return list_to_sort
    else:
        random_pivot_index = random.randint(0, len(list_to_sort) - 1)
        pivot = list_to_sort[random_pivot_index]
        remaining_elements = list_to_sort[:random_pivot_index] + list_to_sort[random_pivot_index + 1 :]

        less_than_pivot = [x for x in remaining_elements if x <= pivot]
        greater_than_pivot = [x for x in remaining_elements if x > pivot]
        return quick_sort(less_than_pivot) + [pivot] + quick_sort(greater_than_pivot)


# Merge sort
def merge_sort(list_to_sort):
    """
    Sort the input list using the merge sort algorithm.

    Parameters:
    -----------
    list_to_sort (list):
        The list of elements to be sorted.

    Returns:
    --------
    list:
        The sorted list.

    Notes:
    ------
    1. Time complexity:
    - Pesimistic case: O(n log n)
    - Average case: O(n log n)
    - Optimistic case: O(n log n)
    2. Space complexity: O(n) (due to the temporary arrays used for merging)
    3. Stability: Stable (if implemented properly)
    4. In-place: No
    """
    if len(list_to_sort) > 1:
        mid = len(list_to_sort) // 2
        left = list_to_sort[:mid]
        right = list_to_sort[mid:]

        # sorting by reccurrence
        merge_sort(left)
        merge_sort(right)

        i, j, k = 0, 0, 0  # left, mid, right

        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                list_to_sort[k] = left[i]
                i += 1
            else:
                list_to_sort[k] = right[j]
                j += 1
            k += 1

        while i < len(left):
            list_to_sort[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            list_to_sort[k] = right[j]
            j += 1
            k += 1

    return list_to_sort


# Shell sort
def shell_sort(list_to_sort):
    """
    Sort the input list using the shell sort algorithm.

    Parameters:
    -----------
    list_to_sort (list):
        The list of elements to be sorted.

    Returns:
    --------
    list:
        The sorted list.

    Notes:
    ------
    1. Time complexity:
    - Pesimistic case: O(n^2) (depends on the gap sequence used)
    - Average case: O(n log n) (depends on the gap sequence used)
    - Optimistic case: O(n) (when the list is already sorted)
    2. Space complexity: O(1)
    3. Stability: Not stable
    4. In-place: Yes
    """
    n = len(list_to_sort)
    gap = n // 2

    while gap > 0:
        for i in range(gap, n):
            temp = list_to_sort[i]
            j = i

            while j >= gap and list_to_sort[j - gap] > temp:
                list_to_sort[j] = list_to_sort[j - gap]
                j -= gap

            list_to_sort[j] = temp

        gap //= 2

    return list_to_sort


# Heap sort
def heap_sort(list_to_sort):
    """
    Sort the input list using the heap sort algorithm.

    Parameters:
    -----------
    list_to_sort (list):
        The list of elements to be sorted.

    Returns:
    --------
    list:
        The sorted list.

    Notes:
    ------
    1. Time complexity:
    - Pesimistic case: O(n log n)
    - Average case: O(n log n)
    - Optimistic case: O(n log n)
    2. Space complexity: O(1)
    3. Stability: Not stable
    4. In-place: No
    """
    n = len(list_to_sort)

    # Heapify subtree rooted at index i
    def heapify(arr, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and arr[left] > arr[largest]:
            largest = left

        if right < n and arr[right] > arr[largest]:
            largest = right

        # If largest is not root
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)

    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(list_to_sort, n, i)

    # Extract elements one by one
    for i in range(n - 1, 0, -1):
        list_to_sort[0], list_to_sort[i] = list_to_sort[i], list_to_sort[0]  # Move max to end
        heapify(list_to_sort, i, 0)

    return list_to_sort


# Counting sort
def counting_sort(list_to_sort):
    """
    Sort the input list using the counting sort algorithm.

    Parameters:
    -----------
    list_to_sort (list):
        The list of non-negative integers to be sorted.

    Returns:
    --------
    list:
        The sorted list.

    Notes:
    ------
    1. Time complexity:
    - Pesimistic case: O(n + m)
    - Average case: O(n + m)
    - Optimistic case: O(n + m)
    2. Space complexity: O(m)
    3. Stability: Stable
    4. In-place: No

    m is size of the range of input values (max_value - min_value + 1).
    Counting sort is efficient for sorting integers when the range of input values (m) is not significantly greater than the number of elements (n).
    """
    if not list_to_sort:
        return list_to_sort

    max_value = max(list_to_sort)
    count = [0] * (max_value + 1)

    # Count occurrences
    for num in list_to_sort:
        count[num] += 1

    # Reconstruct sorted array
    sorted_arr = []
    for value, frequency in enumerate(count):
        sorted_arr.extend([value] * frequency)

    return sorted_arr
