import math
import random

from tocas.AbstrakteRinge import RingElement, RingTupel
from tocas.Restklassenringe import Restklassenring, RestklassenringElement
from tocas.Polynomringe import PolynomringElement

from ha.polynom_restklassenring import PolynomRestklassenringElement

from projekt.abstrakte_gruppen import AdditiveGruppenElement


def _ring_tupel_zwei_adisch(self):
    zwei_adisch = 0
    laenge = 0
    for k in self.koeffizienten:
        (w, l) = k.zwei_adisch()
        if laenge > 0:
            zwei_adisch <<= l
        zwei_adisch += w
        laenge += l
    return (zwei_adisch, laenge)


def _restklassenring_element_zwei_adisch(self):
    return (self.wert, math.ceil(math.log2(self.ring.modulus)))


def _polynomring_element_zwei_adisch(self):
    return self.koeffizienten.zwei_adisch()


def _polynom_restklassenring_element_zwei_adisch(self):
    return (self.wert.zwei_adisch()[0], self.ring.modulus.zwei_adisch()[1])


RingTupel.zwei_adisch = _ring_tupel_zwei_adisch
RestklassenringElement.zwei_adisch = _restklassenring_element_zwei_adisch
PolynomringElement.zwei_adisch = _polynomring_element_zwei_adisch
PolynomRestklassenringElement.zwei_adisch = _polynom_restklassenring_element_zwei_adisch


def generiere_original_walk(g, h, r, n_s):
    """Gibt eine walk Funktion zurück

    (Gleiche Werte müssen nicht mehrfach neu berechnet werden.)
    """
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
    if not isinstance(n_s, int):
        raise TypeError('Parameter n_s ist nicht vom Typ  int')

    g_pre = []
    for j in range(n_s):
        # deterministischer (psuedo) Zufallswert
        # identischer Wert für identischen Index j
        random.seed(j)
        u = random.randrange(0, r)
        v = random.randrange(0, r)

        g_pre.append(mult(exp(g, u), exp(h, v)))

    def walk(x, a: RestklassenringElement, b: RestklassenringElement):
        """Die ursprüngliche (originale) Walk Funktion von Pollard.

        Parameter g_pre ist eine Liste von vorberechneten Werten, die
        mit der Funktion g_vorberechnen vorberechnet werden muss.
        """
        if not isinstance(x, type(g)):
            raise TypeError(
                'Parameter x ist nicht vom selben Typ wie g')
        if not isinstance(a, RestklassenringElement):
            raise TypeError(
                'Parameter a ist nicht vom Typ  RestklassenringElement')
        if not isinstance(b, RestklassenringElement):
            raise TypeError(
                'Parameter b ist nicht vom Typ  RestklassenringElement')
        if a.ring != b.ring:
            raise TypeError(
                'Elemente a und b liegen nicht im selben Restklassenring')
        if not isinstance(n_s, int):
            raise TypeError('Parameter n_s ist nicht vom Typ  int')

        S_x = x.zwei_adisch()[0] % n_s

        # gleiche pseudo Zufallswerte wie in Funktion g_vorberechnen
        random.seed(S_x)
        u = a.ring.element(random.randrange(0, a.ring.modulus))
        v = a.ring.element(random.randrange(0, a.ring.modulus))

        if S_x == 0:
            a = 2 * a
            b = 2 * b
            x = exp(x, 2)
        else:
            a = a + u
            b = b + v
            x = mult(x, g_pre[S_x])

        return (x, a, b)

    return walk


def floyd_cycle_rho(g, h, r: int, n_s=256, walk_generator=generiere_original_walk):
    """Pollards Rho Methode mittels Floyd Cycle Suche."""
    if isinstance(g, RingElement):
        if not isinstance(h, RingElement):
            raise TypeError(
                'Parameter h ist nicht vom selben Typ wie Parameter g')
    elif isinstance(g, AdditiveGruppenElement):
        if not isinstance(h, AdditiveGruppenElement):
            raise TypeError(
                'Parameter h ist nicht vom selben Typ wie Parameter g')
    else:
        raise TypeError(
            'Parameter sind nicht vom Typ RingElement oder AdditiveGruppeElement')
    if not isinstance(r, int):
        raise TypeError('Parameter r ist nicht vom Typ  int')

    F_r = Restklassenring(r)

    walk = walk_generator(g, h, r, n_s)

    x_1 = g
    a_1 = F_r.eins
    b_1 = F_r.null

    (x_2, a_2, b_2) = walk(x_1, a_1, b_1)

    while x_1 != x_2:
        (x_1, a_1, b_1) = walk(x_1, a_1, b_1)
        (x_2, a_2, b_2) = walk(*walk(x_2, a_2, b_2))

    if b_1 == b_2:
        raise ValueError('h kann nicht aus g erzeugt werden')

    return ((a_2 - a_1) * (b_1 - b_2) ** -1).wert
