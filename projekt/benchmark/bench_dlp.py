import os
import sys

sys.path.append(os.getcwd())

import time
import math

from tocas import Restklassenring

from projekt.rho import floyd_cycle_rho, brent_cycle_rho, distinguished_rho
from projekt.kaenguru import kaenguru

F = Restklassenring(32416190071)
g = F.element(32316469506)
r = 5778287 # = org(g) (ist prim)
a = 50
h = g ** 50 # = 2262438373


def time_fn(fn, n=100):
    min_time = math.inf
    max_time = 0
    avg_time = 0

    for _ in range(n):
        start = time.process_time()
        fn()
        elapsed = time.process_time() - start

        min_time = min(min_time, elapsed)
        max_time = max(max_time, elapsed)
        avg_time += elapsed

    avg_time /= n

    return min_time, max_time, avg_time

def floyd(n_s):
    assert floyd_cycle_rho(g, h, r, n_s=n_s) == a

def brent(n_s):
    assert brent_cycle_rho(g, h, r, n_s=n_s) == a

def distinguished(n_d, n_s):
    #assert distinguished_rho(g, h, r, n_d, n_s=n_s) == a
    distinguished_rho(g, h, r, n_d, n_s=n_s)

def kaenguru_fn(n_d, n_s):
    assert kaenguru(g, h, r, 0, F.modulus, n_d, n_s=n_s) == a

if __name__ == '__main__':
    print('floyd')
    print(*time_fn(lambda: floyd(32), 10))
    print('brent')
    print(*time_fn(lambda: brent(32), 10))
    print('distinguished')
    print(*time_fn(lambda: distinguished(7, 32), 10))
    print('kaenguru')
    print(*time_fn(lambda: kaenguru_fn(7, 32), 10))
