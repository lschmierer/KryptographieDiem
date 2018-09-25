import sys

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

if __name__ == '__main__':
    labels = []
    data = []

    with open(sys.argv[1], "r") as file:
        i = 0
        for line in file:
            if i % 2 == 0:
                labels += [line.strip()]
            else:
                data += [[float(x) for x in line.split()]]
            i += 1

    for i in range(1, len(labels)):
        plt.plot(data[0], data[i], label=labels[i])
    plt.ylabel('Laufzeit in Sekunden')
    plt.legend()
    plt.show()
