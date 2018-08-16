import os
import sys

sys.path.append(os.getcwd())

import time
import math

from tocas import Restklassenring

from projekt.rho import floyd_cycle_rho, brent_cycle_rho, distinguished_rho
from projekt.kaenguru import kaenguru


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


def floyd(n_s):
    assert floyd_cycle_rho(g, h, r, n_s=n_s) == a


def brent(n_s):
    assert brent_cycle_rho(g, h, r, n_s=n_s) == a


def distinguished(n_d, n_s):
    assert distinguished_rho(g, h, r, n_d, n_s=n_s) == a


def kaenguru_fn(n_d, n_s):
    assert kaenguru(g, h, r, 0, r, n_d, n_s=n_s) == a


if __name__ == '__main__':
    print('floyd')
    print(*time_fn(lambda: floyd(32), ITERATIONS))
    print('brent')
    print(*time_fn(lambda: brent(32), ITERATIONS))
    print('distinguished')
    print(*time_fn(lambda: distinguished(8, 32), ITERATIONS))
    print('kaenguru')
    print(*time_fn(lambda: kaenguru_fn(8, 32), ITERATIONS))
