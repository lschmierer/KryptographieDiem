import copy
import math

from tocas import Polynomring, PolynomringElement, Restklassenring


def _polynom_div(a: PolynomringElement, b: PolynomringElement):
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


def _polynom_floordiv(a: PolynomringElement, b: PolynomringElement):
    return _polynom_div(a, b)[0]


def _polynom_mod(a: PolynomringElement, b: PolynomringElement):
    return _polynom_div(a, b)[1]


PolynomringElement.__floordiv__ = _polynom_floordiv
PolynomringElement.__mod__ = _polynom_mod


def _polynom_ExtGGT(a: PolynomringElement, b: PolynomringElement):
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


def _polynom_ext_ggt(self: Polynomring, a: PolynomringElement, b: PolynomringElement):
    if not (isinstance(a, PolynomringElement) and isinstance(b, PolynomringElement)):
        raise TypeError('Argumente nicht vom Typ PolynomringElement')

    if a.ring != self or b.ring != self:
        raise TypeError('PolynomringElement nicht im Polynomring')

    return Polynomring.ExtGGT(a, b)


Polynomring.ExtGGT = staticmethod(_polynom_ExtGGT)
Polynomring.ext_ggt = _polynom_ext_ggt


def _primes(n):
    divisors = [d for d in range(2, n//2+1) if n % d == 0]
    return [d for d in divisors if
            all(d % od != 0 for od in divisors if od != d)]


def _polynom_irreduzibel(f: PolynomringElement):
    if not isinstance(f.basisring, Restklassenring):
        raise TypeError('Bassisring muss Restklassenring sein')

    n = [int(f.grad / p) for p in _primes(f.grad)]

    for i in range(1, len(n) + 1):
        h = (f.ring.variable ** f.basisring.modulus **
             n[i] - f.ring.variable) % f
        g = Polynomring.ExtGGT(f, h)
        if g != f.ring.eins:
            return False
    g = (f.ring.variable ** f.basisring.modulus ** f.grad - f.ring.variable) % f
    if g == f.ring.null:
        return True
    return False


PolynomringElement.irreduzibel = _polynom_irreduzibel
