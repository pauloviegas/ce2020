import random
import matplotlib.pyplot as plt

from operator import itemgetter
from itemgenerate import read_file
from utils import display


def generate_population(items, capacity, pop_size, number_items):
    keys = ['id', 'weight', 'value', 'fitness']
    population = []
    for i in range(pop_size):
        dict_ind = {key: 0 for key in keys}
        dict_ind.update({'id': i + 1})
        population = (generate_individual(items, capacity, number_items, i, dict_ind, population))
    population = sorted(population, key=itemgetter('fitness'), reverse=True)
    return population


def generate_individual(items, capacity, number_items, id, dict_ind, pop_list):
    for x in range(number_items):
        dict_ind.update({'id': id + 1})
        alleles = []
        allele = random.choice(items)
        if allele not in alleles:
            dict_ind.update({'weight': dict_ind.get('weight') + allele[0]})
            dict_ind.update({'value': dict_ind.get('value') + allele[1]})
    dict_ind.update({'fitness': fitness(dict_ind.get('weight'), dict_ind.get('value'), capacity)})
    pop_list.append(dict_ind.copy())

    return pop_list


def fitness(weight, value, capacity):
    fit = weight / value
    if weight > capacity:
        fit = 0
    return fit


def save_fitness(file_name, population, generation, execution):
    best_fitness = population[0]['fitness']
    fitness_average = sum(individual['fitness'] for individual in population) / len(population)
    with open("results/" + file_name + "_run_" + str(execution + 1) + ".txt", "a") as file:
        file.write(str(generation + 1) + ', ' + str(best_fitness) + ', ' + str(fitness_average) + '\n')


def mutation(individual, capacity):
    new_individual = individual
    new_individual.update({'weight': new_individual.get('weight') * random.uniform(0.8, 1.3)})
    new_individual.update({'value': new_individual.get('value') * random.uniform(0.8, 1.3)})
    new_individual.update({'fitness': fitness(new_individual.get('weight'), new_individual.get('value'), capacity)})
    return new_individual


def crossover(individual, population, capacity):
    male = individual
    female = population[random.randint(0, len(population) - 1)]

    while male == female:
        female = population[random.randint(0, len(population) - 1)]

    child1 = {}
    child2 = {}

    child1.update({'id': 0})
    child1.update({'weight': male.get('weight')})
    child1.update({'value': female.get('value')})

    child2.update({'id': 0})
    child2.update({'weight': female.get('weight')})
    child2.update({'value': male.get('value')})

    child1.update({'fitness': fitness(child1.get('weight'), child1.get('value'), capacity)})
    child2.update({'fitness': fitness(child2.get('weight'), child2.get('value'), capacity)})

    return child1, child2


def selection(old_population, new_population, pop_size):
    total_population = old_population + new_population
    total_population = sorted(total_population, key=itemgetter('fitness'), reverse=True)
    return total_population[0: pop_size]


def evolve_population(population, mutation_rate, crossover_rate, capacity):
    new_population = []
    index = 1
    for ind in population:
        if mutation_rate > random.random():
            individual = mutation(ind, capacity)
            individual.update({'id': index})
            index += 1
            new_population.append(individual)
        if crossover_rate > random.random():
            individual1, individual2 = crossover(ind, population, capacity)
            individual1.update({'id': index})
            index += 1
            individual2.update({'id': index})
            index += 1
            new_population.append(individual1)
            new_population.append(individual2)
    return new_population


def best_pop(populacao):
    populacao.sort(key=itemgetter(1), reverse=True)
    return populacao[0]


def average_pop(populacao):
    return sum([fit for cromo, fit in populacao]) / len(populacao)


# Main function
def main(file_name, pop_size, num_items, max_generation, mutation_rate, crossover_rate, executions, mode, immigrants):
    items, capacity = read_file(file_name)
    if mode == 1:
        for execution in range(0, executions):
            population = generate_population(items, capacity, pop_size, num_items)
            stat = []
            stat_avg = []
            for generation in range(0, max_generation):
                save_fitness(file_name, population, generation, execution)
                stat.append(population[0]['fitness'])
                stat_avg.append(sum(individual['fitness'] for individual in population) / len(population))
                new_population = evolve_population(population, mutation_rate, crossover_rate, capacity)
                population = selection(population, new_population, pop_size)
            display(stat, stat_avg, execution)
    elif mode == 2:
        for execution in range(0, executions):
            population = generate_population(items, capacity, pop_size, num_items)
            stat = []
            stat_avg = []
            for generation in range(0, max_generation):
                save_fitness(file_name, population, generation, execution)
                stat.append(population[0]['fitness'])
                stat_avg.append(sum(individual['fitness'] for individual in population) / len(population))
                new_population = evolve_population(population, mutation_rate, crossover_rate, capacity)
                population = selection(population, new_population, pop_size)
            display(stat, stat_avg, execution)
    # elif mode == 3:
    #     for execution in range(0, executions):
    #         population = generate_population(items, capacity, pop_size)
    #         stat = []
    #         stat_avg = []
    #         for generation in range(0, max_generation):
    #             save_fitness(file_name, population, generation, execution)
    #             stat.append(population[0]['fitness'])
    #             stat_avg.append(sum(individual['fitness'] for individual in population) / len(population))
    #             new_population = evolve_population(population, mutation_rate, crossover_rate, items, capacity)
    #             population = selection(population, new_population, pop_size)
    #         display(stat, stat_avg, execution)


# main(file_name, pop_size, num_items, max_generation, mutation_rate, crossover_rate, executions, mode, immigrants):
main('average_uncorrelated', 100, 10, 50, 0.05, 0.6, 5, 2, 0.3)
