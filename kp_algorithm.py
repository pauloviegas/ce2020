import random

from itertools import islice
from operator import itemgetter
from itemgenerate import read_file
from utils import display


def generate_population(items, capacity, pop_size, number_items):
    keys = ['id', 'alleles', 'weight', 'value', 'fitness']
    population = []
    for i in range(pop_size):
        dict_ind = {key: 0 for key in keys}
        dict_ind.update({'id': i + 1})
        population = (generate_individual(items, capacity, number_items, dict_ind, population))
    population = sorted(population, key=itemgetter('fitness'), reverse=True)
    return population


def generate_individual(items, capacity, number_items, dict_ind, population):
    alleles = []
    for x in range(number_items):
        insert_allele(items, alleles, dict_ind)
    dict_ind.update({'fitness': fitness(dict_ind.get('weight'), dict_ind.get('value'), capacity)})
    dict_ind.update({'alleles': alleles})
    population.append(dict_ind.copy())

    return population


def insert_allele(items, allele_list, dict_ind):
    allele = random.choice(items)
    if allele not in allele_list:
        allele_list.append(allele)
        dict_ind.update({'weight': dict_ind.get('weight') + allele[0]})
        dict_ind.update({'value': dict_ind.get('value') + allele[1]})
    else:
        insert_allele(items, allele_list, dict_ind)


def fitness(weight, value, capacity):
    fit = weight / value
    if weight > capacity:
        fit = 0
    return fit


def save_fitness(file_name, population, generation, execution, mod):
    best_fitness = population[0]['fitness']
    fitness_average = sum(individual['fitness'] for individual in population) / len(population)
    with open("results/" + file_name + "_mod_" + str(mod) + "_run_" + str(execution + 1) + ".txt", "a") as file:
        file.write(str(generation + 1) + ', ' + str(best_fitness) + ', ' + str(fitness_average) + '\n')


def mutation(individual, capacity, mutation_rate, mod):
    new_individual = individual.copy()
    new_individual.update({'weight': 0})
    new_individual.update({'value': 0})
    new_alleles = []
    for allele in individual.get('alleles'):
        if mutation_rate > random.random() or mod == 3:
            new_allele = (allele[0] * random.uniform(0.8, 1.2), allele[1] * random.uniform(0.8, 1.2))
        else:
            new_allele = allele
        new_alleles.append(new_allele)
        new_individual.update({'weight': new_individual.get('weight') + new_allele[0]})
        new_individual.update({'value': new_individual.get('value') + new_allele[1]})
    new_individual.update({'alleles': new_alleles})
    new_individual.update({'fitness': fitness(new_individual.get('weight'), new_individual.get('value'), capacity)})
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
              'fitness': 0}
    child2 = {'id': 0,
              'alleles': 0,
              'weight': 0,
              'value': 0,
              'fitness': 0}
    child1_alleles = []
    child2_alleles = []
    for i in range(len(male.get('alleles'))):
        if i < (len(male.get('alleles')) / 2):
            child1_alleles.append(male.get('alleles')[i])
            child2_alleles.append(female.get('alleles')[i])
        else:
            child1_alleles.append(female.get('alleles')[i])
            child2_alleles.append(male.get('alleles')[i])
        child1.update({'weight': child1.get('weight') + child1_alleles[i][0]})
        child1.update({'value': child1.get('value') + child1_alleles[i][1]})
        child2.update({'weight': child2.get('weight') + child2_alleles[i][0]})
        child2.update({'value': child2.get('value') + child2_alleles[i][1]})
    child1.update({'alleles': child1_alleles})
    child2.update({'alleles': child2_alleles})
    child1.update({'fitness': fitness(child1.get('weight'), child1.get('value'), capacity)})
    child2.update({'fitness': fitness(child2.get('weight'), child2.get('value'), capacity)})

    return child1, child2


def selection(old_population, new_population, pop_size, items, capacity, number_items, mod, immigrant_percentage,
              mutation_rate):
    total_population = old_population + new_population
    total_population = sorted(total_population, key=itemgetter('fitness'), reverse=True)
    total_population = total_population[0: pop_size]
    if mod == 2:
        immigrant_insertion(items, capacity, number_items, total_population, immigrant_percentage)
    if mod == 3:
        mutation_mod(capacity, mutation_rate, total_population, immigrant_percentage,mod)
    total_population = sorted(total_population, key=itemgetter('fitness'), reverse=True)
    return total_population


def immigrant_insertion(items, capacity, number_items, population, immigrant_percentage):
    for individual in islice(population, int(len(population) - (len(population) * immigrant_percentage)), None, None):
        alleles = []
        for x in range(number_items):
            insert_allele(items, alleles, individual)
        individual.update({'fitness': fitness(individual.get('weight'), individual.get('value'), capacity)})
        individual.update({'alleles': alleles})


def mutation_mod(capacity, mutation_rate, population, immigrant_percentage, mod):
    for individual in islice(population, int(len(population) - (len(population) * immigrant_percentage)), None, None):
        mutant_individual = mutation(population[0], capacity, mutation_rate, mod)
        individual.update({'weight': mutant_individual.get('weight')})
        individual.update({'value': mutant_individual.get('value')})
        individual.update({'fitness': fitness(mutant_individual.get('weight'), mutant_individual.get('value'), capacity)})
        individual.update({'alleles': mutant_individual.get('alleles')})


def evolve_population(population, mutation_rate, crossover_rate, capacity, mod):
    new_population = []
    index = 1
    for ind in population:
        individual = mutation(ind, capacity, mutation_rate, mod)
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
def main(file_name, pop_size, num_items, max_generation, mutation_rate, crossover_rate, executions, mod,
         immigrant_percentage):
    items, capacity = read_file(file_name)
    for execution in range(executions):
        population = generate_population(items, capacity, pop_size, num_items)
        stat = []
        stat_avg = []
        for generation in range(max_generation):
            save_fitness(file_name, population, generation, execution, mod)
            new_population = evolve_population(population, mutation_rate, crossover_rate, capacity, mod)
            population = selection(population, new_population, pop_size, items, capacity, num_items, mod,
                                   immigrant_percentage, mutation_rate)
            stat.append(population[0]['fitness'])
            stat_avg.append(sum(individual['fitness'] for individual in population) / len(population))
        display(stat, stat_avg, execution)


# main(file_name, pop_size, num_items, max_generation, mutation_rate, crossover_rate, executions, mod, immigrants):

main('average_uncorrelated', 100, 10, 100, 0.1, 0.7, 5, 3, 0.3)
