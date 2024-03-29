import os
import sys
import math
import signal

sys.path.append(os.getcwd())

import time
import math

from tocas import Restklassenring

from projekt.baby_step_giant_step import baby_step_giant_step
from projekt.rho import floyd_cycle_rho, brent_cycle_rho, distinguished_rho
from projekt.kaenguru import kaenguru


ITERATIONS = 3


#p = [1000000009, 1000003111, 1000003051, 1000001581, 1000001237, 1000000349, 1000002791]
#g = [112345, 2458792, 54466, 16315, 188, 321, 12]
#r = [167, 1061, 10433, 111857, 1012147, 10869569, 100000279]

p = [20000000219, 20000000291, 20000000357, 20000000333, 
     20000000113, 20000000201, 20000000431, 20000000179, 20000000117]
g = [5487742, 96933, 1014328, 144678, 33036, 89, 255, 6, 10]
r = [281, 733, 12101, 96419, 1039069, 5882353, 222222227, 1111111121, 5000000029]


def signal_handler(signum, frame):
    raise Exception()


def time_fn(fn, n=100):
    signal.signal(signal.SIGALRM, signal_handler)

    times = []

    for _ in range(n):
        while True:
            try:
                signal.alarm(120)
                start = time.process_time()
                fn()
                elapsed = time.process_time() - start
                break
            except Exception as e:
                print(e)
                continue

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
    assert floyd_cycle_rho(g, h, r, n_s=2*int(math.log10(r))) == a


def brent(g, h, r, a, n_s):
    assert brent_cycle_rho(g, h, r, n_s=2*int(math.log10(r))) == a


def distinguished(g, h, r, a, n_s):
    assert distinguished_rho(g, h, r, round(math.log10(r)), n_s=2*int(math.log10(r))) == a


def kaenguru_fn(g, h, r, a, n_s):
    assert kaenguru(g, h, r, 0, r, round(math.log10(r)), n_s=2*int(math.log10(r))) == a


if __name__ == '__main__':
    print('r')
    print(*r)
    print('baby_step_giant_step')
    print(*bench(lambda g, h, r, a: bsgs(g, h, r, a)))
    print('floyd')
    print(*bench(lambda g, h, r, a: floyd(g, h, r, a, 16)))
    print('brent')
    print(*bench(lambda g, h, r, a: brent(g, h, r, a, 16)))
    print('distinguished')
    print(*bench(lambda g, h, r, a: distinguished(g, h, r, a, 16)))
    print('kaenguru')
    print(*bench(lambda g, h, r, a: kaenguru_fn(g, h, r, a, 16)))
