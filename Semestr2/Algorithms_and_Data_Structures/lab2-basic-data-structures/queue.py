class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return not self.items

    def enqueue(self, item):
        pass

    def dequeue(self):
        pass

    def size(self):
        return len(self.items)

    def print_queue(self):
        print("Queue contents:", self.items)


class FIFOQueue(Queue):
    def enqueue(self, item):
        """
        Enqueue an item to the end of the queue.

        Parameters:
        -----------
        item:
            The item to be added to the queue.

        Notes:
        ------
        Time Complexity: O(1)
        """
        self.items.append(item)

    def dequeue(self):
        """
        Dequeue an item from the beggining of the queue.

        Notes:
        ------
        Time Complexity: O(1)
        """
        if self.is_empty():
            raise IndexError("Dequeue from an empty queue")
        return self.items.pop(0)


class LIFOQueue(Queue):
    def enqueue(self, item):
        """
        Enqueue an item from the beggining of the queue.

        Parameters:
        -----------
        item:
            The item to be added to the queue.

        Notes:
        ------
        Time Complexity: O(1)
        """
        self.items.append(item)

    def dequeue(self):
        """
        Dequeue an item from the end of the queue.

        Notes:
        ------
        Time Complexity: O(1)
        """
        if self.is_empty():
            raise IndexError("Dequeue from an empty queue")
        return self.items.pop()


def conduct_experiment(queue_class: Queue, num_elements: int = 7, to_dequeue: int = 3):
    queue = queue_class()
    for i in range(num_elements):
        queue.enqueue(i)
    print(f"{queue_class.__name__} after enqueuing {num_elements} elements:")
    queue.print_queue()
    for _ in range(to_dequeue):
        queue.dequeue()
    print(f"{queue_class.__name__} after dequeuing {to_dequeue} elements:")
    queue.print_queue()


# 1. FIFO queue
conduct_experiment(FIFOQueue)

# 2. LIFO queue
conduct_experiment(LIFOQueue)
