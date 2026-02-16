import random
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from timeit import default_timer as timer


def generate_random_elements(N, M):
    l = [[0, 0] for _ in range(N)]
    for i in range(N):
        l[i][0] = random.randint(1, 1000)  # value
        l[i][1] = random.randint(1, int(M / 2))  # size
    return l


# M - capacity of knapsack
# N - number of elements
# table_of_elements - list with value and weight of a single element
# l - table with results


def knapsack_problem(M, N, table_of_elements):
    l = [[0 for _ in range(M + 1)] for _ in range(N + 1)]
    for i in range(1, N + 1):
        for j in range(M + 1):
            vi = table_of_elements[i - 1][0]
            wi = table_of_elements[i - 1][1]
            if wi > j:
                l[i][j] = l[i - 1][j]
            else:
                l[i][j] = max(l[i - 1][j], vi + l[i - 1][j - wi])
    return l[N][M]


def plot_graph(elements, times, title, xaxis, save=False):
    data_plot = pd.DataFrame({xaxis: elements, "Time [s]": times})
    plot = sns.lineplot(x=xaxis, y="Time [s]", data=data_plot, marker='o')
    plot.set_title(title, fontdict={'size': 15}, wrap=True)
    plt.yscale('log')
    plt.xscale('log')

    if save:
        plt.savefig('plot.png')
    plt.show()


def conduct_experiments(elements_to_experiment):
    times = {i: [] for i in elements_to_experiment}

    for nr_of_elements in elements_to_experiment:
        M = 100
        table_of_elements = generate_random_elements(nr_of_elements, M)
        start = timer()
        knapsack_problem(M, nr_of_elements, table_of_elements)
        end = timer()
        times[nr_of_elements].append(end - start)

    for size_of_knapsack in elements_to_experiment:
        N = 100
        table_of_elements = generate_random_elements(N, size_of_knapsack)
        start = timer()
        knapsack_problem(size_of_knapsack, N, table_of_elements)
        end = timer()
        times[size_of_knapsack].append(end - start)

    for i in elements_to_experiment:
        table_of_elements = generate_random_elements(i, i)
        start = timer()
        knapsack_problem(i, i, table_of_elements)
        end = timer()
        times[i].append(end - start)

    print('Summary:', end='\n\n')

    print('Time vs number of elements to choose from')
    print([round(times[i][0], 6) for i in elements_to_experiment], end='\n\n')

    print('Time vs size of the knapsack')
    print([round(times[i][1], 6) for i in elements_to_experiment], end='\n\n')

    print('Time vs both number of elements to choose from and size of the knapsack')
    print([round(times[i][2], 6) for i in elements_to_experiment], end='\n\n')

    plot_graph(
        elements_to_experiment,
        [times[i][0] for i in elements_to_experiment],
        'Time of computation vs number of elements to choose from',
        'Number of elements',
    )
    plot_graph(
        elements_to_experiment,
        [times[i][1] for i in elements_to_experiment],
        'Time of computation vs size of the knapsack',
        'Size of knapsack',
    )

    plot_graph(
        elements_to_experiment,
        [times[i][2] for i in elements_to_experiment],
        'Time of computation vs both number of elements to choose from and size of the knapsack',
        'Number of elements',
    )


if __name__ == '__main__':
    conduct_experiments([5, 10, 20, 100, 500, 2000, 5000, 10000])
