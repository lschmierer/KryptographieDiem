import math

from tocas.AbstrakteRinge import RingElement

import ha.polynom_extension
import ha.restklassen_extension

import projekt.hash_extension
from projekt.abstrakte_gruppen import AdditiveGruppenElement


def baby_step_giant_step(g, h, r: int):
    "Baby-Step-Giant-Step Algorithmus zur Lösung des diskreten Logarithmus-Problems"

    if isinstance(g, RingElement):
        if not isinstance(h, RingElement):
            raise TypeError(
                'Parameter h ist nicht vom selben Typ wie Parameter g')
        if g.ring != h.ring:
            raise ValueError('g und h sind nicht im selben Ring')

        def mult(a, b):
            return a * b

        def exp(a, b):
            return a ** b

        def neutral(a):
            return a.ring.eins

    elif isinstance(g, AdditiveGruppenElement):
        if not isinstance(h, AdditiveGruppenElement):
            raise TypeError(
                'Parameter h ist nicht vom selben Typ wie Parameter g')
        if g.gruppe != h.gruppe:
            raise ValueError('g und h sind nicht zur selben Gruppe')

        def mult(a, b):
            return a + b

        def exp(a, b):
            return a * b

        def neutral(a):
            return a.gruppe.neutral

    else:
        raise TypeError(
            'Parameter sind nicht vom Typ RingElement oder AdditiveGruppeElement')

    m = math.ceil(math.sqrt(r))
    hashtable = dict()
    x = neutral(g)
    for i in range(0, m+1):
        hashtable[x] = i
        x = mult(g, x)
    u = exp(g, -m)
    y, j = h, 0
    while hashtable.get(y) is None:
        y = mult(y, u)
        j += 1
    i = hashtable.get(y)
    if i is not None:
        return i + m * j
    else:
        raise ValueError('h kann nicht aus g erzeugt werden')
