import os
import sys

sys.path.append(os.getcwd())

import time
import math

from tocas import Restklassenring

from projekt.rho import distinguished_rho
from projekt.parallel_rho import parallel_rho

WORKER1 = 6
WORKER2 = 11
ITERATIONS = 10

F = Restklassenring(32416190071)
g = F.element(32316469506)
r = 5778287  # = org(g) (ist prim)
a = 2778286
h = g ** a  # = 3805914789


def time_fn(fn, n=100):
    times = []

    for _ in range(n):
        start = time.process_time()
        fn()
        elapsed = time.process_time() - start

        times += [elapsed]

    return times


def distinguished(n_d, n_s):
    assert distinguished_rho(g, h, r, n_d, n_s=n_s) == a


def parallel(n_d, n_s, worker):
    assert parallel_rho(g, h, r, n_d, n_s=n_s, worker=worker) == a


if __name__ == '__main__':
    print('distinguished')
    print(*time_fn(lambda: distinguished(8, 32), ITERATIONS))
    print('parallel (5 cores)')
    print(*time_fn(lambda: parallel(8, 32, WORKER1), ITERATIONS))
    print('parallel (11 cores)')
    print(*time_fn(lambda: parallel(8, 32, WORKER2), ITERATIONS))
