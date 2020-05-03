# To run: python -c "from knapsack_algorithm import test; test()"
# python -c "from knapsack_algorithm import main; main('average_uncorrelated', 100, 2, 0.2,  0.2, 1)"
# Imports
import random
from operator import itemgetter
from itemgenerate import read_file


def generate_population(items, capacity, pop_size):
    population = []
    for i in range(pop_size):
        individual = generate_individual(items, capacity)
    individual.sort(key=itemgetter(1), reverse=True)
    #population.append([individual, fitness(individual, capacity)])
    population.append([individual, fitness(individual, capacity)])
    return population


def generate_individual(items, capacity):
    # Variables
    individual = []
    total_weight = 0

    while total_weight < capacity:
        allele = random.choice(items)
        if allele not in individual:
            total_weight += allele[0]
            individual.append(allele)
    print(individual)
    return individual


def mutation(individual, items, capacity):
    old_individual = individual[0]
    new_allele = random.randint(0, len(items) - 1)

    while items[new_allele] in old_individual:
        new_allele = random.randint(0, len(items) - 1)

    allele = random.randint(0, len(old_individual) - 1)
    old_individual[allele] = items[new_allele]
    new_indivvidual = [old_individual, fitness(old_individual, capacity)]
    return new_indivvidual


def crossover(individual, population, capacity):
    male = individual[0]
    female = population[random.randint(0, len(population) - 1)][0]

    while male == female:
        female = population[random.randint(0, len(population) - 1)][0]

    crossover_point = random.randint(0, len(individual[0]) - 1)
    child1 = male[:crossover_point] + female[crossover_point:]
    child2 = male[crossover_point:] + female[:crossover_point]
    return [child1, fitness(child1, capacity)], [child2, fitness(child2, capacity)]


def fitness(individual, capacity):
    total_weight = 0
    total_value = 0
    for allele in individual:
        total_weight += allele[0]
        total_value += allele[1]

    if total_weight > capacity:
        total_weight = 0
    return total_value


def selection(old_population, new_population, pop_size):
    total_population = old_population + new_population
    total_population.sort(key=lambda x: x[1], reverse=True)
    return total_population[0: pop_size - 1]


def evolve_population(population, mutation_rate, crossover_rate, items, capacity):
    new_population = []
    for i in population:
        if mutation_rate > random.random():
            individual = mutation(i, items, capacity)
            new_population.append(individual)
        if crossover_rate > random.random():
            individual1, individual2 = crossover(i, population, capacity)
            new_population.append(individual1)
            new_population.append(individual2)
    return new_population


def save_fitness(file_name, population, generation, execution):
    best_fitness = population[0][1]
    fitness_average = sum(individual[1] for individual in population) / len(population)
    # print(best_fitness)
    # print(fitness_average)
    with open("results/" + file_name + "_run_" + str(execution + 1) + ".txt", "a") as file:
        file.write(str(generation + 1) + ', ' + str(best_fitness) + ', ' + str(fitness_average) + '\n')


# Main function
def main(file_name, pop_size, max_generation, mutation_rate, crossover_rate, executions):
    items, capacity = read_file(file_name)
    for execution in range(0, executions):
        population = generate_population(items, capacity, pop_size)
        for generation in range(0, max_generation):
            save_fitness(file_name, population, generation, execution)
            new_population = evolve_population(population, mutation_rate, crossover_rate, items, capacity)
            population = selection(population, new_population, pop_size)


def test():
    items, capacity = read_file('average_uncorrelated')
    population = generate_population(items, capacity, 2)
    # print(population)

    # items, capacity = read_file('average_uncorrelated')
    # r = range(round(capacity * 0.9), round(capacity * 1.1))
    # i = 0
    # while i not in r:
    #     print(i)
    #     i+=1
    # print(sum(item[0] for item in items))