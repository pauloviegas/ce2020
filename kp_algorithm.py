import random
from operator import itemgetter
from itemgenerate import read_file


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
            print('individual {} allele {}: {}'.format(id + 1, x + 1, allele))
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
    # with open("results/" + file_name + "_run_" + str(execution + 1) + ".txt", "a") as file:
    with open("results/" + file_name + ".txt", "a") as file:
        file.write(str(best_fitness) + ', ' + str(fitness_average) + '\n')


items, capacity = read_file('average_uncorrelated')
pop = generate_population(items, capacity, 3, 45)
# best_fitness = pop[0]['fitness']
# fitness_average = sum(individual['fitness'] for individual in pop) / len(pop)
save_fitness('average_uncorrelated', pop, 0, 0)
print(pop)
# Main function
# def main(file_name, pop_size, max_generation, mutation_rate, crossover_rate, executions, mode):
#     items, capacity = read_file(file_name)
#     print(capacity)
#     if mode == 1:
#         for execution in range(0, executions):
#             population = generate_population(items, capacity, pop_size)

# for generation in range(0, max_generation):
#     save_fitness(file_name, population, generation, execution)
#     new_population = evolve_population(population, mutation_rate, crossover_rate, items, capacity)
#     population = selection(population, new_population, pop_size)
# elif mode == 2:
#     for execution in range(0, executions):
#         population = generate_population(items, capacity, pop_size)
#         for generation in range(0, max_generation):
#             save_fitness(file_name, population, generation, execution)
#             new_population = evolve_population(population, mutation_rate, crossover_rate, items, capacity)
#             population = selection(population, new_population, pop_size)
# elif mode == 3:
#     for execution in range(0, executions):
#         population = generate_population(items, capacity, pop_size)
#         for generation in range(0, max_generation):
#             save_fitness(file_name, population, generation, execution)
#             new_population = evolve_population(population, mutation_rate, crossover_rate, items, capacity)
#             population = selection(population, new_population, pop_size)

# main('average_uncorrelated', 10, 300, 0.05, 0.7, executions, mode)
