import matplotlib.pyplot as plt

    
def display(best, average, mod):
    generations = list(range(len(best)))
    plt.figure()
    plt.title('Average Performance over runs (MOD {}):'.format(mod))
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.plot(generations, best, label='Best')
    plt.plot(generations, average, label='Average')
    plt.legend(loc='best')
    plt.show()