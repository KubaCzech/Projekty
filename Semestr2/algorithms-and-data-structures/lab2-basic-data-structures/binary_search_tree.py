import random
from time import perf_counter


class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key


def insert_node(root, key):
    if root is None:
        return Node(key)
    else:
        if root.val == key:
            return root
        elif root.val < key:
            root.right = insert_node(root.right, key)
        else:
            root.left = insert_node(root.left, key)
    return root


def remove_node(root, element):
    if root is None:
        return root

    if element < root.val:
        root.left = remove_node(root.left, element)
    elif element > root.val:
        root.right = remove_node(root.right, element)
    else:
        # Case 1 & 2: Node with only one child or no child
        if root.left is None:
            return root.right
        elif root.right is None:
            return root.left

        # Case 3: Node with two children
        root.val = min_value(root.right)
        root.right = remove_node(root.right, root.val)

    return root


def check_existance(root, n):
    if root is None:
        return False
    if root.val == n:
        return True
    elif n > root.val:
        return check_existance(root.right, n)
    else:
        return check_existance(root.left, n)


def min_value(root):
    while root.left:
        root = root.left
    return root.val


def max_value(root):
    while root.right is not None:
        root = root.right
    return root.val


def check_size(root):
    if root is None:
        return 0
    return 1 + check_size(root.left) + check_size(root.right)


def inorder_traversal(root):
    if root:
        inorder_traversal(root.left)
        print(root.val)
        inorder_traversal(root.right)


def preorder_traversal(root):
    if root:
        print(root.val)
        preorder_traversal(root.left)
        preorder_traversal(root.right)


def postorder_traversal(root):
    if root:
        postorder_traversal(root.left)
        postorder_traversal(root.right)
        print(root.val)


def create_tree_from_list(l):
    l.sort()

    def build_balanced_bst(elements, low, high):
        if low > high:
            return None

        mid = (low + high) // 2
        node = Node(elements[mid])

        node.left = build_balanced_bst(elements, low, mid - 1)
        node.right = build_balanced_bst(elements, mid + 1, high)

        return node

    return build_balanced_bst(l, 0, len(l) - 1)


def create_random_tree(size_of_tree):
    data = random.sample(range(size_of_tree * 10), size_of_tree)
    root = create_tree_from_list(data)

    return root


def conduct_experiments():
    sizes = [10, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 50000]
    results = {}
    results_avg = []
    for _ in range(10):
        for i in sizes:
            tree = create_random_tree(i)
            time_start = perf_counter()
            check_existance(tree, i * 10 + 1)
            time_end = perf_counter()
            time_passed = time_end - time_start
            if i not in results.keys():
                results[i] = []
            results[i].append(time_passed)
    for i in range(10):
        results_avg.append(sum(results[sizes[i]]) / len(results[sizes[i]]))
    print("Times taken for each size to check existence of a non-existent element (on average):")
    for time, size in zip(results_avg, sizes):
        print(f"Size: {size:<10} Time: {time:.10f} seconds")


# 1. Inserting and deleting nodes in a BST
r = Node(50)
r = insert_node(r, 30)
r = insert_node(r, 20)
r = insert_node(r, 40)
r = insert_node(r, 70)
r = insert_node(r, 85)
print("Tree with inserted nodes:")
inorder_traversal(r)
print()

r = remove_node(r, 70)
print("Tree after deleting node with value 70:")
inorder_traversal(r)
print()

# 2. Checking for the existence of a value in the BST
print("Checking existence of existing value in the BST:", check_existance(r, 40))
print("Checking existence of non-existing value in the BST:", check_existance(r, 70), end="\n\n")

# 3. Finding the minimum and maximum values in the BST
print("Min:", min_value(r))
print("Max:", max_value(r), end="\n\n")

# 4. Calculating the size of the BST
print("Size of the tree:", check_size(r), end="\n\n")

# 5. Traversing the BST in different orders (in-order, pre-order, post-order)
print("In-order Traversal:")
inorder_traversal(r)
print()

print("Pre-order Traversal:")
preorder_traversal(r)
print()

print("Post-order Traversal:")
postorder_traversal(r)
print()

# 6. Creating a random balanced BST
random_tree = create_random_tree(10)
inorder_traversal(random_tree)

# 7. Conducting experiments to analyze the time complexity of search operations in a BST
conduct_experiments()
