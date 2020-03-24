# To run: python -c "from itemgenerate import main; main(attrs)"
# Imports
import random
import numpy as np


# Weights and Values generate
# Generate the items with uncorrelated weights and values
def uncorrelated(qnt_items, max_value):
    items = []
    for i in range(qnt_items):
        weight = random.uniform(1, max_value)
        value = random.uniform(1, max_value)
        items.append((weight, value))
        # print("%s: Weight - %s, Value - %s" % (i, weight, value))
    return items


# Generate the items with a weakly correlation between weights and values
def weakly_correlated(qnt_items, max_value):
    items = []
    for i in range(qnt_items):
        weight = random.uniform(1, max_value)
        value = weight + random.uniform(1, max_value)
        items.append((weight, value))
    return items


# Generate the items with a strong correlation between weights and values
def strong_correlated(qnt_items, max_value, r):
    items = []
    for i in range(qnt_items):
        weight = random.uniform(1, max_value)
        value = weight + r
        items.append((weight, value))
    return items


# Capacity generate
# Generate the capacity of the bag based of the max value
def restrictive(max_value):
    capacity = 2 * max_value
    return round(capacity)


# Generate the capacity of the bag based of the average of the items
def average(items):
    # capacity = np.mean(items, axis=0)[0]
    capacity = 0.5 * sum(item[0] for item in items)
    return round(capacity)


# Data storage
# Function to save the data into a files
def save_data(file_name, file, capacity):
    with open('items/' + file_name + '.txt', 'w') as fp:
        fp.write(str(capacity) + '\n')
        fp.write('\n'.join('%s, %s' % x for x in file))


# Function to read the data, return a list of items and the capacity of the bag
def read_file(file_name):
    count_line = 0
    capacity = 0
    items = []
    with open('items/' + file_name + '.txt') as f:
        lines = f.readlines()
        for line in lines:
            myarray = np.fromstring(line, dtype=float, sep=',')
            if count_line != 0:
                items.append(tuple(myarray))
            else:
                capacity = int(myarray[0])
                count_line += 1
    return items, capacity


# Function to execute and generate all
# Main function
def main(qnt_items, max_value, r):
    # Case 01
    items = uncorrelated(qnt_items, max_value)
    capacity = restrictive(max_value)
    save_data('restrictive_uncorrelated', items, capacity)
    # Case 02
    items = weakly_correlated(qnt_items, max_value)
    capacity = restrictive(max_value)
    save_data('restrictive_weakly_correlated', items, capacity)
    # Case 03
    items = strong_correlated(qnt_items, max_value, r)
    capacity = restrictive(max_value)
    save_data('restrictive_strong_correlated', items, capacity)
    # Case 04
    items = uncorrelated(qnt_items, max_value)
    capacity = average(items)
    save_data('average_uncorrelated', items, capacity)
    # Case 05
    items = weakly_correlated(qnt_items, max_value)
    capacity = average(items)
    save_data('average_weakly_correlatede', items, capacity)
    # Case 06
    items = strong_correlated(qnt_items, max_value, r)
    capacity = average(items)
    save_data('average_strong_correlated', items, capacity)
