import copy

from tocas import Polynomring, PolynomringElement


def polyFloorDiv(a: PolynomringElement, b: PolynomringElement):
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

    return PolynomringElement(q_koeffizienten, a.ring)


PolynomringElement.__floordiv__ = polyFloorDiv


def polyExtGGT(a: PolynomringElement, b: PolynomringElement):
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
    return a, u, v


Polynomring.ExtGGT = staticmethod(polyExtGGT)
Polynomring.ext_ggt = polyExtGGT
