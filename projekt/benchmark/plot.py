import sys

import matplotlib.pyplot as plt

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

    print('min & max & avg')
    for i in range(len(labels)):
        print(labels[i])

        min_time = min(data[i])
        max_time = max(data[i])
        avg_time = sum(data[i]) / len(data[i])

        print('{:1.3f} & {:1.3f} & {:1.3f}'.format(
            min_time, max_time, avg_time))

    plt.boxplot(data, labels=labels)
    plt.ylabel('Laufzeit in Sekunden')
    plt.show()
