import random
from multiprocessing import Process, Queue, Value

from tocas.AbstrakteRinge import RingElement
from tocas.Restklassenringe import Restklassenring

import projekt.zwei_adisch_extension
from projekt.abstrakte_gruppen import AdditiveGruppenElement
from projekt.rho import generiere_original_walk


def _randrange(n):
    # Das ist schneller als random.randrange(0, n)
    return int(random.random() * n)


def parallel_rho(g, h, r: int, n_d: int, walk_generator=generiere_original_walk, n_s=256, worker=4):
    '''Parallelisierte Version der Rho Methode mit distinuished points.'''
    if isinstance(g, RingElement):
        if not isinstance(h, RingElement):
            raise TypeError(
                'Parameter h ist nicht vom selben Typ wie Parameter g')

        def mult(a, b):
            return a * b

        def exp(a, b):
            return a ** b
    elif isinstance(g, AdditiveGruppenElement):
        if not isinstance(h, AdditiveGruppenElement):
            raise TypeError(
                'Parameter h ist nicht vom selben Typ wie Parameter g')

        def mult(a, b):
            return a + b

        def exp(a, b):
            return a * b
    else:
        raise TypeError(
            'Parameter sind nicht vom Typ RingElement oder AdditiveGruppeElement')
    if not isinstance(r, int):
        raise TypeError('Parameter r ist nicht vom Typ  int')
    if not isinstance(n_d, int):
        raise TypeError('Parameter n_d ist nicht vom Typ  int')
    if not isinstance(n_s, int):
        raise TypeError('Parameter n_s ist nicht vom Typ  int')

    F_r = Restklassenring(r)

    walk = walk_generator(g, h, F_r, n_s)

    new_found_points = Queue()
    log_found = Value('b', 0)

    def find_distinguished_points(F_r, walk, queue, stop):
        while not stop.value:
            a = F_r.element(_randrange(F_r.modulus))
            b = F_r.element(_randrange(F_r.modulus))
            x = mult(exp(g, a.wert), exp(h, b.wert))

            while x.zwei_adisch()[0] & ((2 ** n_d) - 1) != 0:
                (x, a, b) = walk(x, a, b)

            queue.put((x, a, b))

    for _ in range(worker):
        Process(target=find_distinguished_points, args=(
            F_r, walk, new_found_points, log_found)).start()

    distinguished_points = {}
    while True:
        (x_1, a_1, b_1) = new_found_points.get()

        if x_1 in distinguished_points:
            break
        else:
            distinguished_points[x_1] = (a_1, b_1)

    (a_2, b_2) = distinguished_points[x_1]
    log_found.value = 1

    if b_1 == b_2:
        raise ValueError('h kann nicht aus g erzeugt werden')

    return ((a_2 - a_1) * (b_1 - b_2) ** -1).wert
