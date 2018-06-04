import copy

from tocas import Polynomring, PolynomringElement


def polynom_div(a: PolynomringElement, b: PolynomringElement):
    """Polynomdivision ohne Rest"""
    a_koeffizienten = copy.copy(a.koeffizienten.koeffizienten)
    b_koeffizienten = b.koeffizienten.koeffizienten
    q_koeffizienten = []

    while a_koeffizienten and len(a_koeffizienten) >= len(b_koeffizienten):
        t = a_koeffizienten[-1] / b_koeffizienten[-1]
        q_koeffizienten = [t] + q_koeffizienten

        for i in range(len(b_koeffizienten)):
            a_koeffizienten[len(a_koeffizienten) -
                            len(b_koeffizienten) + i] -= t * b_koeffizienten[i]

        del a_koeffizienten[-1]

    q = PolynomringElement(q_koeffizienten, a.ring)
    r = PolynomringElement(a_koeffizienten, a.ring)

    return q, r


def polynom_floordiv(a: PolynomringElement, b: PolynomringElement):
    return polynom_div(a, b)[0]


def polynom_mod(a: PolynomringElement, b: PolynomringElement):
    return polynom_div(a, b)[1]


PolynomringElement.__floordiv__ = polynom_floordiv
PolynomringElement.__mod__ = polynom_mod


def polynom_ExtGGT(a: PolynomringElement, b: PolynomringElement):
    if not (isinstance(a, PolynomringElement) and isinstance(b, PolynomringElement)):
        raise TypeError('Argumente nicht vom Typ PolynomringElement')

    if a.basisring != b.basisring:
        raise ValueError(
            'PolynomringElement haben nicht den gleichen Grundring')

    u, v = a.ring.eins, a.ring.null
    s, t = a.ring.null, a.ring.eins
    while b != a.ring.null:
        q = a // b
        a, b = b, a - q * b
        u, s = s, u - q * s
        v, t = t, v - q * t
    return a.ring.eins, u // a, v // a


def polynom_ext_ggt(self: Polynomring, a: PolynomringElement, b: PolynomringElement):
    if not (isinstance(a, PolynomringElement) and isinstance(b, PolynomringElement)):
        raise TypeError('Argumente nicht vom Typ PolynomringElement')

    if a.ring != self or b.ring != self:
        raise TypeError('PolynomringElement nicht im Polynomring')

    return Polynomring.ExtGGT(a, b)


Polynomring.ExtGGT = staticmethod(polynom_ExtGGT)
Polynomring.ext_ggt = polynom_ext_ggt
