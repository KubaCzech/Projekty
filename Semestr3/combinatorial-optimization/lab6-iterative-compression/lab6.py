n, k = [int(el) for el in input().split()]
G = []
for i in range(n):
    neighs = [int(el) for el in input().split()]
    G.append(neighs)
print(G)

G2 = []
S = set()
for v in range(n):  # iterate over all vertices
    vlist = []
    for v2 in G[v]:  # iterate over all neighbours of current vertex
        if v2 < len(G2):
            G2[v2].append(v)
            vlist.append(v2)
    G2.append(vlist)
    S.add(v)
    Slist = list(S)
    if len(S) <= k:
        continue
    for sub_id in range(2 ** (k + 1)):
        T = set()  # new solution
        for i in range(k + 1):
            if (sub_id >> i) & 1 == 1:  # if bit is 1 we add it to new solution
                T.add(Slist[i])
            else:
                for neigh in G2[Slist[i]]:
                    T.add(neigh)
        if len(T) <= k:
            S = T
            break
    if len(S) <= k:  # checking if solution is ok
        print(S)
    else:
        print("Haven't found a solution")
