from copy import deepcopy
# in order to use first generate an initial solution (using for example shortest edge or other greedy algorithm)
# graph a matrix where entries are the distances between cities (symmetric matrix) 
# M

# {0: set({1, 2}), ...} egdes / solution

p = 3

matrix = [[-1, 10, 1, 1], 
          [10, -1, 1, 1], 
          [1, 1, -1, 1],
          [1, 1, 1, -1]]

initial_solution = {0: set([1, 3]), 1: set([0, 2]), 2: set([1, 3]), 3: set([2, 0])}
vertices = [] # list of vertices 
edges = set() # list of tuples, every tuple is an edge
total = 0

def LinKerninghan(sol): # sol solution to modify
    global vertices, edges, total
    # if list of verts is even adding ..., if list of verts is odd ...
    v_last = vertices[-1] # last visited vertex 
    if len(vertices) % 2 == 1: # the edges we ll be removing from our solution
        for v2 in sol[v_last]: # looking with whom v_last is adajcent 
            if (v_last, v2) in edges:
                continue 
            total -= matrix[v_last][v2]
            vertices.append(v2)
            edges.add((v_last, v2))
            edges.add((v2, v_last))
            result = LinKerninghan(sol)
            if result:
                return result
            # else we need to del everything we've added
            total += matrix[v_last][v2]
            vertices.pop()
            edges.remove((v_last, v2))
            edges.remove((v2, v_last))
    else: # even edge 
        for v2 in range(len(matrix)):
            if v2 == v_last:
                continue
            if len(vertices) - 1 == 2*p and v_last != vertices[0]:
                continue
            if v2 in sol[v_last]:
                continue
            if total + matrix[v_last][v2] >= 0:
                continue
            if (v_last, v2) in edges:
                continue
            total += matrix[v_last][v2]
            vertices.append(v2)
            edges.add((v_last, v2))
            edges.add((v2, v_last))
            
            if v2 == vertices[0]:
                result = check(sol)
                if result:
                    vertices = []
                    edges = set()
                    total = 0
                    return result

            result = LinKerninghan(sol)
            if result:
                return result
            # else we need to del everything we've added
            total -= matrix[v_last][v2]
            vertices.pop()
            edges.remove((v_last, v2))
            edges.remove((v2, v_last))
    
    return None


def modify(sol):
    s2 = deepcopy(sol)
    for i in range(1, len(vertices)):
        v1 = vertices[i-1]
        v2 = vertices[i]
        if i % 2 == 1: # considering an egde that will be deleted 
            s2[v1].remove(v2)
            s2[v2].remove(v1)
        else: # an edge to be added
            s2[v1].add(v2)
            s2[v2].add(v1)

    return s2
            

def check(sol): # check wheter solution is a correct solution of tsp
    s2 = modify(sol)
    curr = 0
    visited = set()
    visited.add(0)
    for i in range(len(matrix)):
        prev = curr
        for v2 in s2[curr]:
            if v2 not in visited or (v2 == 0 and i == len(matrix)-1):
                visited.add(v2)
                curr = v2
                break
        if curr == prev:
            return None
        
    return s2


vertices.append(0)

for v in range(len(matrix)):
    vertices[0] = v
    result = LinKerninghan(initial_solution)
    if result:
        print(result)
        break
