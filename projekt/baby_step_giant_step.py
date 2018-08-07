import math

from tocas.AbstrakteRinge import RingElement, Ganzzahlring, RingTupel
from tocas.Restklassenringe import Restklassenring, RestklassenringElement
from tocas.Polynomringe import Polynomring, PolynomringElement

import ha.polynom_extension
import ha.restklassen_extension
from ha.polynom_restklassenring import PolynomRestklassenring, PolynomRestklassenringElement

from projekt.abstrakte_gruppen import AdditiveGruppenElement
from projekt.weierstrass_kurvengruppe import WeierstrassKurvengruppenElement
from projekt.edwards_kurvengruppe import EdwardsKurvengruppenElement


def _ring_tupel_hash(self):
    return hash((self.laenge, tuple(self.koeffizienten)))


def _restklassenring_hash(self):
    return hash(self.modulus)


def _restklassenring_element_hash(self):
    return hash((self.wert, self.ring))


def _polynomring_hash(self):
    return hash(self.basisring)


def _polynomring_element_hash(self):
    return hash((self.koeffizienten, self.ring))


def _polynom_restklassenring_hash(self):
    return hash(self.modulus)


def _polynom_restklassenring_element_hash(self):
    return hash((self.wert, self.ring))


RingTupel.__hash__ = _ring_tupel_hash
Restklassenring.__hash__ = _restklassenring_hash
RestklassenringElement.__hash__ = _restklassenring_element_hash
Polynomring.__hash__ = _polynomring_hash
PolynomringElement.__hash__ = _polynomring_element_hash
PolynomRestklassenring.__hash__ = _polynom_restklassenring_hash
PolynomRestklassenringElement.__hash__ = _polynom_restklassenring_element_hash


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
    while(hashtable.get(y) is None):
        y = mult(y, u)
        j += 1
    i = hashtable.get(y)
    if(i is not None):
        return i + m * j
    else:
        raise ValueError('h kann nicht aus g erzeugt werden')
