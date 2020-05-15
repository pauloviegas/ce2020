import random

from itertools import islice
from operator import itemgetter
from itemgenerate import read_file
from utils import display


def generate_population(items, capacity, pop_size):
    keys = ['id', 'alleles', 'weight', 'value', 'fitness', 'mutation', 'crossover']
    population = []
    for i in range(pop_size):
        dict_ind = {key: 0 for key in keys}
        dict_ind.update({'id': i + 1})
        population.append(generate_individual(items, capacity, dict_ind))
    population = sorted(population, key=itemgetter('fitness'), reverse=True)
    return population


# def generate_individual(items, capacity, number_items, dict_ind):
#     alleles = []
#     for x in range(number_items):
#         insert_allele(items, alleles, dict_ind)
#     dict_ind.update({'alleles': alleles})
#     dict_ind = fitness(dict_ind, capacity)
#
#     return dict_ind

def generate_individual(items, capacity, individual):
    test_weight = 0
    alleles = []
    while test_weight < capacity:
        allele = random.choice(items)
        if allele not in alleles:
            alleles.append(allele)
            test_weight += allele[0]
    individual.update({'alleles': alleles})
    individual = fitness(individual, capacity)
    return individual

# def fitness(individual, capacity):
#     individual.update({"weight": 0})
#     individual.update({"value": 0})
#     individual.update({"fitness": 0})
#     for allele in individual.get('alleles'):
#         individual.update({'weight': individual.get('weight') + allele[0]})
#         individual.update({'value': individual.get('value') + allele[1]})
#     individual.update({'fitness': individual.get('value') / individual.get('weight')})
#     if individual.get('weight') > capacity:
#         individual.update({'fitness': 0})
#     return individual

def fitness(individual, capacity):
    individual.update({"weight": 0})
    individual.update({"value": 0})
    individual.update({"fitness": 0})
    for allele in individual.get('alleles'):
        individual.update({'weight': individual.get('weight') + allele[0]})
        individual.update({'value': individual.get('value') + allele[1]})
    if individual.get('weight') < capacity:
        individual.update({'fitness': individual.get('value')})
    else:
        individual.update({'fitness': 0})
    return individual


def save_fitness(file_name, population, generation, execution, mod):
    best_fitness = population[0]['fitness']
    best_weight = population[0]['weight']
    best_value = population[0]['value']
    fitness_average = sum(individual['fitness'] for individual in population) / len(population)
    weight_average = sum(individual['weight'] for individual in population) / len(population)
    value_average = sum(individual['value'] for individual in population) / len(population)
    with open("results/" + file_name + "_mod_" + str(mod) + "_run_" + str(execution + 1) + ".txt", "a") as file:
        file.write(str(generation) + ', ' + str(best_fitness) + ', ' + str(best_weight) + ', '
                   + str(best_value) + ', ' + str(fitness_average) + ', ' + str(weight_average) + ', '
                   + str(value_average) + '\n')


def mutation(individual, capacity, mutation_rate, items):
    new_individual = individual.copy()
    new_alleles = []
    for allele in individual.get('alleles'):
        if mutation_rate > random.random():
            new_allele = random.choice(items)
            while new_allele in individual.get('alleles'):
                new_allele = random.choice(items)
            new_individual.update({'mutation': 1})
        else:
            new_allele = allele
        new_alleles.append(new_allele)
    new_individual.update({'alleles': new_alleles})
    new_individual = fitness(new_individual, capacity)
    return new_individual


def crossover(individual, population, capacity):
    male = individual
    female = population[random.randint(0, len(population) - 1)]

    while male == female:
        female = population[random.randint(0, len(population) - 1)]

    child1 = {'id': 0,
              'alleles': 0,
              'weight': 0,
              'value': 0,
              'fitness': 0,
              'mutation': 0,
              'crossover': 1
              }
    child2 = {'id': 0,
              'alleles': 0,
              'weight': 0,
              'value': 0,
              'fitness': 0,
              'mutation': 0,
              'crossover': 1
              }
    child1_alleles = []
    child2_alleles = []
    male_point = random.randrange(len(male.get('alleles')))
    female_point = random.randrange(len(female.get('alleles')))

    for i in range(0, male_point):
        child1_alleles.append(male.get('alleles')[i])
    for i in range(0, female_point):
        child2_alleles.append(female.get('alleles')[i])
    for i in range(male_point, len(male.get('alleles'))):
        child1_alleles.append(male.get('alleles')[i])
    for i in range(female_point, len(female.get('alleles'))):
        child2_alleles.append(female.get('alleles')[i])
    child1.update({'alleles': child1_alleles})
    child2.update({'alleles': child2_alleles})
    child1 = fitness(child1, capacity)
    child2 = fitness(child2, capacity)

    return child1, child2


def selection(old_population, new_population, pop_size, items, capacity, mod, immigrant_percentage,
              mutation_rate):
    total_population = old_population + new_population
    total_population = sorted(total_population, key=itemgetter('fitness'), reverse=True)
    total_population = total_population[0: pop_size]
    if mod == 2:
        total_population = immigrant_insertion(items, capacity, total_population, immigrant_percentage)
    if mod == 3:
        mutation_mod(capacity, mutation_rate, total_population, immigrant_percentage, mod)
    total_population = sorted(total_population, key=itemgetter('fitness'), reverse=True)
    return total_population


def immigrant_insertion(items, capacity, population, immigrant_percentage):
    keys = ['id', 'alleles', 'weight', 'value', 'fitness', 'mutation', 'crossover']
    for individual in islice(population, int(len(population) - (len(population) * immigrant_percentage)), None, None):
        temp_individual = {key: 0 for key in keys}
        temp_individual = generate_individual(items, capacity, temp_individual)
        individual.update({'weight': temp_individual.get('weight')})
        individual.update({'value': temp_individual.get('value')})
        individual.update({'fitness': temp_individual.get('fitness')})
        individual.update({'alleles': temp_individual.get('alleles')})
        individual.update({'mutation': 0})
        individual.update({'crossover': 0})
    return population

def mutation_mod(capacity, mutation_rate, population, immigrant_percentage, mod):
    best_individual = population[0].copy()
    for individual in islice(population, int(len(population) - (len(population) * immigrant_percentage)), None, None):
        mutant_individual = mutation(population[0], capacity, mutation_rate, mod)
        individual.update({'weight': mutant_individual.get('weight')})
        individual.update({'value': mutant_individual.get('value')})
        individual.update({'fitness': fitness(mutant_individual.get('weight'), mutant_individual.get('value'), capacity)})
        individual.update({'alleles': mutant_individual.get('alleles')})


def evolve_population(population, mutation_rate, crossover_rate, capacity, items):
    new_population = []
    index = 1
    for ind in population:
        individual = mutation(ind, capacity, mutation_rate, items)
        if individual.get('mutation') == 1:
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


# Main function
def main(file_name, pop_size, max_generation, mutation_rate, crossover_rate, executions, mod,
         immigrant_percentage):
    items, capacity = read_file(file_name)
    items_graph = [0] * len(items)
    for execution in range(0, executions):
        population = generate_population(items, capacity, pop_size)
        stat = []
        stat_avg = []
        save_fitness(file_name, population, 1, execution, mod)

        for generation in range(2, max_generation + 1):
            new_population = evolve_population(population, mutation_rate, crossover_rate, capacity, items)
            population = selection(population, new_population, pop_size, items, capacity, mod,
                                   immigrant_percentage, mutation_rate)
            save_fitness(file_name, population, generation, execution, mod)
            stat.append(population[0]['fitness'])
            stat_avg.append(sum(individual['fitness'] for individual in population) / len(population))
        display(stat, stat_avg, execution)


# main(file_name, pop_size, max_generation, mutation_rate, crossover_rate, executions, mod, immigrant_percentage):

main('average_uncorrelated', 100, 300, 0.03, 0.3, 5, 1, 0.3)
