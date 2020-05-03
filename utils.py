import matplotlib.pyplot as plt

    
def display(best, average, execution):
    generations = list(range(len(best)))
    plt.figure()
    plt.title('Performance over generations. Run number: {}'.format(execution + 1))
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.plot(generations, best, label='Best')
    plt.plot(generations, average, label='Average')
    plt.legend(loc='best')
    plt.show()
    
def display_stat_n(boa,average_best):
    generations = list(range(len(boa)))
    plt.title('Performance over runs')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.plot(generations, boa, label='Best of All')
    plt.plot(generations,average_best,label='Average of Bests')
    plt.legend(loc='best')
    plt.show()