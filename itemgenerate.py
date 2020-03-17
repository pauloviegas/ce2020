# Imports
import random
from numpy import mean

# To run: python -c "from itemgenerate import uncorrelated; uncorrelated(5,5)"


# Weights and Values generate
# Generate the items with uncorrelated weights and values
def uncorrelated(qnt_items, max_value):
    items = []
    for i in range(qnt_items):
        weight = random.uniform(1, max_value)
        value = random.uniform(1, max_value)
        items.append((weight, value))
        # print("%s: Weight - %s, Value - %s" % (i, weight, value))
    print(items)
    return items


# Generate the items with a weakly correlation between weights and values
def weakly_correlated(qnt_items, max_value):
    items = []
    for i in range(qnt_items):
        weight = random.uniform(1, max_value)
        value = weight + random.uniform(1, max_value)
        items.append((weight, value))
    print(items)
    return items


# Generate the items with a strong correlation between weights and values
def strong_correlated(qnt_items, max_value, r):
    items = []
    for i in range(qnt_items):
        weight = random.uniform(1, max_value)
        value = weight + r
        items.append((weight, value))
    print(items)
    return items


# Capacity generate
# Generate the capacity of the bag based of the max value
def restrictive(max_value):
    capacity = 2 * max_value
    print(capacity)
    return capacity


# Generate the capacity of the bag based of the average of the items
def average(items):
    capacity = 0.5 * mean(items, axis=0)[0]
    print(capacity)
    return capacity


# Main
def main():
    # Variables
    qnt_items = 10
    max_value = 10
    r = 10

    # Case 01
    items = uncorrelated(qnt_items, max_value)
    capacity = restrictive(max_value)
    # Case 02
    items = weakly_correlated(qnt_items, max_value)
    capacity = restrictive(max_value)
    # Case 03
    items = strong_correlated(qnt_items, max_value, r)
    capacity = restrictive(max_value)

    # Case 04
    items = uncorrelated(qnt_items, max_value)
    capacity = average(items)
    # Case 05
    items = weakly_correlated(qnt_items, max_value)
    capacity = average(items)
    # Case 06
    items = strong_correlated(qnt_items, max_value, r)
    capacity = average(items)
