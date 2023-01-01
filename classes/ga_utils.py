
import numpy as np
import random

from classes.sudoku import Sudoku


def create_generation(population_size, values_to_set):

    population = []
    for i in range(population_size):
        population.append(Sudoku(values_to_set).fill_random())
    return population


def rank_population(population):

    individuals_and_score = {}
    for individual in population:
        individuals_and_score[individual] = individual.fitness()
    return sorted(individuals_and_score, key=individuals_and_score.get)


def pick_from_population(ranked_population, selection_rate, random_selection_rate):

    next_breeders = []

    nb_best_to_select = int(len(ranked_population) * selection_rate)   #best 2000 count hobe
    nb_random_to_select = int(len(ranked_population) * random_selection_rate)

    # Keep n best elements in the population + randomly n other elements (note: might be the same)
    for i in range(nb_best_to_select):
        next_breeders.append(ranked_population[i])
    for i in range(nb_random_to_select):
        next_breeders.append(random.choice(ranked_population))

    # Shuffle everything to avoid having only the best (copyright Tina Turner) at the beginning
    np.random.shuffle(next_breeders)
    return next_breeders


def create_children(next_breeders, nb_children):

    next_population = []
    # Divided by 2: one 'father' and one 'mother'
    for i in range(int(len(next_breeders)/2)):
        for j in range(nb_children):
            # We take father at the beginning of the list, mother at the end (remember that elements have been shuffled)
            next_population.append(create_one_child(next_breeders[i], next_breeders[len(next_breeders) - 1 - i],
                                                    next_breeders[i].get_initial_values()))
    return next_population


def create_children_random_parents(next_breeders, nb_children):

    next_population = []
    # Randomly pick 1 father and 1 mother until new population is filled
    range_val = int(len(next_breeders)/2) * nb_children
    for _ in range(range_val):
        father = random.choice(next_breeders)
        mother = random.choice(next_breeders)
        next_population.append(create_one_child_random_elements(father, mother, father.get_initial_values()))
    return next_population


def create_one_child(father, mother, values_to_set):

    # Avoid having only the whole father or the whole mother
    sudoku_size = father.size()
    crossover_point = np.random.randint(1, sudoku_size - 1)

    child_grids = []
    for i in range(sudoku_size):
        if i < crossover_point: #father mother theke kototuku nibe
            child_grids.append(father.grids()[i])
        else:
            child_grids.append(mother.grids()[i])
    return Sudoku(values_to_set).fill_with_grids(child_grids)


def create_one_child_random_elements(father, mother, values_to_set):

    # Avoid having only the whole father or the whole mother
    sudoku_size = father.size()
    elements_from_mother = np.random.randint(0, sudoku_size, np.random.randint(1, sudoku_size - 1))

    child_grids = []
    for i in range(sudoku_size):
        if i in elements_from_mother:
            child_grids.append(mother.grids()[i])
        else:
            child_grids.append(father.grids()[i])
    return Sudoku(values_to_set).fill_with_grids(child_grids)


def mutate_population(population, mutation_rate):
    population_with_mutation = []
    for individual in population:
        if np.random.random() < mutation_rate:
            individual = individual.swap_2_values()
        population_with_mutation.append(individual)
    return population_with_mutation
