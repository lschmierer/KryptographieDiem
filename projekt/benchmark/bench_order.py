import os
import sys

sys.path.append(os.getcwd())

import time
import math

from tocas import Restklassenring

from projekt.baby_step_giant_step import baby_step_giant_step
from projekt.rho import floyd_cycle_rho, brent_cycle_rho, distinguished_rho
from projekt.kaenguru import kaenguru


ITERATIONS = 3

p = [100003, 1000003, 10000019, 100000007, 1000000007, 10000000019, 100000000003, 1000000000039]
g = [17, 9, 5556, 1536, 2, 36322, 71664, 19978 ]
r = [2381, 166667, 1523, 101833, 500000003, 73259, 1543067, 26005097]


def time_fn(fn, n=100):
    times = []

    for _ in range(n):
        start = time.process_time()
        fn()
        elapsed = time.process_time() - start

        times += [elapsed]

    return times


def bench(fn):
    avg_times = []
    for i in range(len(g)):
        F = Restklassenring(p[i])
        g_i = F.element(g[i])
        a = r[i] - 1
        h_i = g_i ** a

        times = time_fn(lambda: fn(g_i, h_i, r[i], a), ITERATIONS)

        avg_times += [sum(times) / float(len(times))]

    return avg_times


def bsgs(g, h, r, a):
    assert baby_step_giant_step(g, h, r) == a


def floyd(g, h, r, a, n_s):
    assert floyd_cycle_rho(g, h, r, n_s=n_s) == a


def brent(g, h, r, a, n_s):
    assert brent_cycle_rho(g, h, r, n_s=n_s) == a


def distinguished(g, h, r, a, n_d, n_s):
    assert distinguished_rho(g, h, r, n_d, n_s=n_s) == a


def kaenguru_fn(g, h, r, a, n_d, n_s):
    assert kaenguru(g, h, r, 0, r, n_d, n_s=n_s) == a


if __name__ == '__main__':
    print('baby_step_giant_step')
    print(*bench(lambda g, h, r, a: bsgs(g, h, r, a)))
    print('floyd')
    print(*bench(lambda g, h, r, a: floyd(g, h, r, a, 32)))
    print('brent')
    print(*bench(lambda g, h, r, a: brent(g, h, r, a, 32)))
    print('distinguished')
    print(*bench(lambda g, h, r, a: distinguished(g, h, r, a, 8, 32)))
    print('kaenguru')
    print(*bench(lambda g, h, r, a: kaenguru_fn(g, h, r, a, 8, 32)))
