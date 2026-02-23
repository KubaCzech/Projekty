import sys
import random

import numpy as np

score = 0
max_score = 0


# version from 14.01.24

def calculate_maximum_limit_of_books_to_ship(library):
    return int(shipping_count_per_day[library]) * int(days_remaining - signup_times[library])


def read_integers_line() -> [int]:
    return [int(n) for n in next(sys.stdin).split()]


def get_books_available_in_library(library):
    return np.where(availability_of_books_in_libraries[:, library])[0]


def find_best_books_available_in_library(library):
    books_in_library = get_books_available_in_library(library)
    maximum_to_ship = min(
        books_in_library.shape[0],
        calculate_maximum_limit_of_books_to_ship(library)
    )
    return books_in_library[
               np.argsort(books_ratings[books_in_library])
           ][-maximum_to_ship:]


def calculate_scores_sum_of_best_books_in_library(library):
    return np.sum(books_ratings[find_best_books_available_in_library(library)])


def calculate_coefficients(library, book_scores, available_books_in_library, nr_of_days, signup_times,
                           shipping_count_per_day, books_selection):
    maxi_index = min(len(books_selection[library]),
                     (nr_of_days - signup_times[library].item()) * shipping_count_per_day[library].item())
    books = books_selection[library][:maxi_index]
    score = 0
    for i in books:
        score += book_scores[i].item()
    return score / signup_times[library].item()


def dynamic_complement(delta, not_used_libs, signup_times, ships_per_day):
    table = np.zeros((len(not_used_libs) + 1, delta + 1))
    for i in range(1, len(not_used_libs) + 1):
        for j in range(1, delta + 1):
            element = not_used_libs[i - 1]
            wi = signup_times[element]  # weight -> signup
            vi = ships_per_day[element]  # value -> ships per day
            if (wi > j):
                table[i][j] = table[i - 1][j]
            else:
                table[i][j] = max(table[i - 1][j], vi + table[i - 1][j - wi])
    selected_items = []
    w, i = delta, len(not_used_libs)
    while i > 0 and w > 0:
        if table[i, w] != table[i - 1, w]:
            selected_items.append(not_used_libs[i - 1])
            w -= signup_times[not_used_libs[i - 1]]
        i -= 1
    selected_items.sort(key=lambda x: ships_per_day[x])
    return selected_items


def limit_libraries(available_books_in_library, libraries_count, signup_times, shipping_count_per_day, book_scores,
                    nr_of_days,
                    books_selection):  # delete libraries which are not so good -> list of indexes of quality libraries
    libs = []
    libs_used = []
    max_books_possible = np.empty(libraries_count)
    for i in range(libraries_count):
        score = calculate_coefficients(i, book_scores, available_books_in_library, nr_of_days, signup_times,
                                       shipping_count_per_day, books_selection)
        libs.append(score)
    libs = np.argsort(libs)[::-1]
    libs = libs.tolist()
    day = 0
    i = 0

    for index in libs:
        if (day + signup_times[index].item() >= nr_of_days):
            break
        maxi = (nr_of_days - day - signup_times[index].item()) * shipping_count_per_day[index].item()
        max_books_possible[index] = min(
            len(books_selection[index]), maxi)
        day += signup_times[index].item()
        i += 1
    libs_used = libs[:i]  # list with ids of best libraries to choose

    # update information
    total_signup_days = sum(
        signup_times[i].item() for i in libs_used)
    delta = nr_of_days - total_signup_days  # days which will remain not used after signing_up all libraries from above
    if (delta > 0 and len(libs_used) < len(libs)):
        dynamic_items = dynamic_complement(delta, libs[i:], signup_times, shipping_count_per_day)
        for index in dynamic_items:
            if (day + signup_times[index].item() >= nr_of_days):
                break
            maxi = (nr_of_days - day - signup_times[index].item()) * shipping_count_per_day[index].item()
            max_books_possible[index] = min(
                len(books_selection[index]), maxi)
            day += signup_times[index].item()
            i += 1
    else:
        dynamic_items = []

    libs_used.extend(dynamic_items)
    return libs_used, np.array(max_books_possible)


# Reading Input
books_count, libraries_count, days_remaining = read_integers_line()
nr_of_days = days_remaining
_books_scores = np.array(read_integers_line(), dtype=int)
max_score = np.sum(_books_scores)

availability_of_books_in_libraries = np.zeros((books_count, libraries_count), dtype=bool)

signup_times = np.empty(libraries_count, dtype=int)
shipping_count_per_day = np.empty(libraries_count, dtype=int)

books_in_library_count = np.ones(books_count, dtype=int)  # np.ones as there can be books outside of all libraries
book_selection = [[] for i in range(libraries_count)]

for library in range(libraries_count):
    library_books_count, library_signup_time, library_shipping_time = read_integers_line()
    signup_times[library] = library_signup_time
    shipping_count_per_day[library] = library_shipping_time

    books_in_current_library = read_integers_line()
    books_in_current_library.sort(key=lambda x: _books_scores[x])
    book_selection[library] = books_in_current_library

    books_in_library_count[books_in_current_library] += 1
    availability_of_books_in_libraries[books_in_current_library, library] = True

books_ratings = _books_scores / books_in_library_count
libraries_ratings = np.array([
    calculate_scores_sum_of_best_books_in_library(library) for library in range(libraries_count)
]) / signup_times ** 1.25


def evaluate(solution):
    scanned_books = set()
    for selection in solution:
        for book in selection:
            scanned_books.add(book)
    books = np.array(list(scanned_books))
    return sum(_books_scores[books])


# greedy algorithm
def greedy_solution():
    global days_remaining
    global score
    global max_score

    sorted_libraries_by_scores = list(np.argsort(libraries_ratings))

    remaining_library_signup_time = 0
    libs = []
    solution = []
    while days_remaining > 0:
        if remaining_library_signup_time == 0 and sorted_libraries_by_scores:
            library = sorted_libraries_by_scores.pop()  # max score
            remaining_library_signup_time = signup_times[library]

            chosen_books = find_best_books_available_in_library(library)

            if len(chosen_books) > 0:
                score += np.sum(_books_scores[chosen_books])

                libs.append(library)
                solution.append(chosen_books)

                availability_of_books_in_libraries[chosen_books, :] = 0

        remaining_library_signup_time -= 1
        days_remaining -= 1

    score = evaluate(solution)
    return solution, score, libs


def print_output(solution, limited_libraries):
    out = ""
    for i in range(len(limited_libraries)):
        out += f"{limited_libraries[i]} {len(solution[i])}\n"
        out += " ".join(str(b) for b in solution[i]) + "\n"
    sys.stdout.write(f"{len(limited_libraries)}\n")
    sys.stdout.write(out)


# genetic algorithm (working on greedy and dynamic programming solution)
class LibraryChoiceGeneticAlgorithm:
    def __init__(self, av_of_b_i_l, signup_times, shipping_count_per_day, b_in_lib_count, books_scores,
                 limited_libraries, books_selection, max_books_possible):
        self.size_of_population = 50
        self.mutation_probability = 0.5
        self.tournament_size = 4
        self.mating_pool_size = 50

        self.availability_of_books_in_lib = av_of_b_i_l  # array
        self.signup_times = signup_times  # array
        self.shipping_count_per_day = shipping_count_per_day  # array
        self.books_in_library_count = b_in_lib_count  # array
        self.book_scores = books_scores  # array
        self.limited_libraries = limited_libraries  # list with good enough libraries
        self.books_selection = books_selection  # list [[books in lib with id index]]
        self.max_books_possible = max_books_possible  # array

        self.result = self.evolutionary_algorithm()

    def evolutionary_algorithm(self):
        not_improved_gens = 0
        # 1. create and evaluate initial population
        pop = self.create_population()
        population = self.evaluate_population(pop)
        population.sort(key=lambda x: x[1])

        global_maximum = population[0][1]
        solution = population[0][0]
        generations = 200
        while generations > 0 and not_improved_gens < 10:
            # 2. get mating pool to produce offspring
            mating_pool = self.mating_pool(population)

            # 3. get offspring, evaluate and find maximum
            offspring = self.get_offspring(mating_pool)
            best_of_children = self.get_maximum(offspring)
            local_maximum, local_solution = best_of_children[1], best_of_children[0]

            if local_maximum > global_maximum:  # some improvement
                not_improved_gens = 0
                global_maximum = local_maximum
                solution = local_solution
            else:  # no improvement
                not_improved_gens += 1
            population = population + offspring

            # 4. select best solutions with tournament selection
            best = [self.get_maximum(population)]  # we are sure we won't delete our best individual
            for _ in range(self.size_of_population - 1):
                best.append(self.tournament_selection(population))
            population = best[:]
            generations -= 1

        return (solution, global_maximum)

    def evaluate_solution(self, solution):
        # fitness function = sum of book scores for scanned books
        books_scanned = set()
        for lib in solution:
            for book in lib:
                books_scanned.add(book)
        books = np.array(list(books_scanned))
        return sum(self.book_scores[books])

    def evaluate_population(self, population):
        pop_evaluated = []  # list of [solution, its evaluation]
        for solution in population:
            evaluation = self.evaluate_solution(solution)
            pop_evaluated.append([solution, evaluation])
        # highest fitness first
        return pop_evaluated

    def create_single_solution(self):
        solution = []
        for i in self.limited_libraries:
            curr_lib = np.random.choice(a=self.books_selection[i], replace=False, size=int(self.max_books_possible[i]))
            int_lib = curr_lib.tolist()
            solution.append(int_lib)
        return solution

    def create_population(self):
        pop = []
        while len(pop) < self.size_of_population:
            solution = self.create_single_solution()
            pop.append(solution)
        return pop

    def get_maximum(self, population):
        a = max(population,
                key=lambda x: x[1])  # looks for solution with best evaluation; max takes O(n), sort takes O(n log n)
        return a

    def tournament_selection(self, population):
        chosen_solutions = random.choices(population, k=self.tournament_size)
        best_solution = self.get_maximum(chosen_solutions)
        return best_solution

    def mating_pool(self, population):
        mating_pool = []
        for i in range(self.mating_pool_size):  # size of mating pool
            parents = []
            for j in range(2):
                individual_ix = random.randint(0, len(population) - 1)
                individual = population[individual_ix][0]
                parents.append(
                    individual)  # individual is list of [solution, evaluation] of len 1, we need solution so [0][0]
            mating_pool.append(parents)
        return mating_pool

    def mutate(self, sol):
        if np.random.random() < self.mutation_probability:
            for _ in range(int(len(self.limited_libraries) / 4)):
                ix = random.randint(0, len(sol) - 1)
                new_part = np.random.choice(
                    self.books_selection[self.limited_libraries[ix]],
                    size=int(self.max_books_possible[self.limited_libraries[ix]]), replace=False)
                new_part.tolist()
                sol[ix] = new_part
        return sol

    def crossover(self, sol1, sol2):
        child = []
        if (random.random() < 0.7):
            i = random.randint(1, len(sol1) - 1)
            child = sol1[:i] + sol2[i:]
        else:  # no crossover
            if (random.random() > 0.5):
                child = sol1
            else:
                child = sol2
        return child

    def get_offspring(self, mating_pool):
        children = []
        for parents in mating_pool:
            child = self.crossover(parents[0], parents[1])
            child = self.mutate(child)
            score = self.evaluate_solution(child)
            children.append([child, score])
        return children


solution_greedy, score_greedy, limited_libraries_greedy = greedy_solution()
limited_libraries_genetic, max_books_possible = limit_libraries(availability_of_books_in_libraries, libraries_count,
                                                                signup_times, shipping_count_per_day, _books_scores,
                                                                nr_of_days, book_selection)
genetic_solver = LibraryChoiceGeneticAlgorithm(availability_of_books_in_libraries, signup_times, shipping_count_per_day,
                                               books_in_library_count, _books_scores, limited_libraries_genetic,
                                               book_selection, max_books_possible)
solution_genetic, score_genetic = genetic_solver.result

if score_greedy > score_genetic:
    print_output(solution_greedy, limited_libraries_greedy)
else:
    print_output(solution_genetic, limited_libraries_genetic)
