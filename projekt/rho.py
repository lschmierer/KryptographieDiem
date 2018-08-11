import math
import random

from tocas.AbstrakteRinge import RingElement, RingTupel
from tocas.Restklassenringe import Restklassenring, RestklassenringElement
from tocas.Polynomringe import PolynomringElement

from ha.polynom_restklassenring import PolynomRestklassenringElement

import projekt.hash_extension
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


def generiere_original_walk(g, h, F_r, n_s):
    """Generiert die ursprüngliche (originale) Walk Funktion von Pollard."""
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

    if not isinstance(F_r, Restklassenring):
        raise TypeError('Parameter F_r ist nicht vom Typ  Restklassenring')
    if not isinstance(n_s, int):
        raise TypeError('Parameter n_s ist nicht vom Typ  int')

    random.seed(0)

    g_pre = []
    for _ in range(n_s):
        u = F_r.element(random.randrange(0, F_r.modulus))
        v = F_r.element(random.randrange(0, F_r.modulus))

        g_pre.append((u, v, mult(exp(g, u.wert), exp(h, v.wert))))

    def walk(x, a: RestklassenringElement, b: RestklassenringElement):
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

        (u, v, g_S_x) = g_pre[S_x]

        if S_x == 0:
            a = 2 * a
            b = 2 * b
            x = exp(x, 2)
        else:
            a = a + u
            b = b + v
            x = mult(x, g_S_x)

        return (x, a, b)

    return walk


def generiere_additiv_walk(g, h, F_r, n_s):
    """Generiert die additive Walk Funktion nach Pollard."""
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

    if not isinstance(F_r, Restklassenring):
        raise TypeError('Parameter F_r ist nicht vom Typ  Restklassenring')
    if not isinstance(n_s, int):
        raise TypeError('Parameter n_s ist nicht vom Typ  int')

    random.seed(0)

    g_pre = []
    for _ in range(n_s):
        u = F_r.element(random.randrange(0, F_r.modulus))
        v = F_r.element(random.randrange(0, F_r.modulus))

        g_pre.append((u, v, mult(exp(g, u.wert), exp(h, v.wert))))

    def walk(x, a: RestklassenringElement, b: RestklassenringElement):
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

        (u, v, g_S_x) = g_pre[S_x]

        a = a + u
        b = b + v
        x = mult(x, g_S_x)

        return (x, a, b)

    return walk


def floyd_cycle_rho(g, h, r: int, walk_generator=generiere_original_walk, n_s=256):
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

    walk = walk_generator(g, h, F_r, n_s)

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


def brent_cycle_rho(g, h, r: int, walk_generator=generiere_original_walk, n_s=256):
    """Pollards Rho Methode mit Brent's optimierter Suche."""
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

    walk = walk_generator(g, h, F_r, n_s)

    x_1 = g
    a_1 = F_r.eins
    b_1 = F_r.null

    (x_2, a_2, b_2) = walk(x_1, a_1, b_1)

    power = step = 1
    while x_1 != x_2:
        if power == step:
            (x_1, a_1, b_1) = (x_2, a_2, b_2)
            power *= 2
            step = 0
        (x_2, a_2, b_2) = walk(x_2, a_2, b_2)
        step += 1

    if b_1 == b_2:
        raise ValueError('h kann nicht aus g erzeugt werden')

    return ((a_2 - a_1) * (b_1 - b_2) ** -1).wert


def distinguished_rho(g, h, r: int, n_d: int, walk_generator=generiere_original_walk, n_s=256):
    """Pollards Rho Methode mit Brent's optimierter Suche.
    
    Parameter n_d gibt die Anzahl an least-significant bits an
    die null sein müssen, sodass ein Element als distinguished
    Element makiert wird.
    Da wir hier die Python hash Funktion nutzen (die sehr große
    Ganzzahlen als Hash erzeugt), kann es sein, dass bei kleinen
    Ringen kein distinguished Element gefunden wird.
    Bei größeren Ringen sollte das statistisch zu vernachlässigen
    sein."""
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

    F_r = Restklassenring(r)

    walk = walk_generator(g, h, F_r, n_s)

    distinguished_points = {}
    while True:
        a_1 = F_r.element(random.randrange(0, F_r.modulus))
        b_1 = F_r.element(random.randrange(0, F_r.modulus))
        x_1 = mult(exp(g, a_1.wert), exp(h, b_1.wert))

        while hash(x_1) % (2 ** n_d) != 0:
            (x_1, a_1, b_1) = walk(x_1, a_1, b_1)

        if x_1 in distinguished_points:
            break
        else:
            distinguished_points[x_1] = (a_1, b_1)

    (a_2, b_2) = distinguished_points[x_1]

    if b_1 == b_2:
        raise ValueError('h kann nicht aus g erzeugt werden')

    return ((a_2 - a_1) * (b_1 - b_2) ** -1).wert
