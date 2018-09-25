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

    x = list(map(int, data[0]))
    del labels[0]
    del data[0]

    for i in range(len(labels)):
        plt.plot(x, data[i], label=labels[i])
    ax = plt.gca()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlabel('Ordnung')
    plt.ylabel('Laufzeit in Sekunden')
    plt.legend()
    plt.show()
