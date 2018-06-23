import copy
import math

from tocas import Polynomring, PolynomringElement, Restklassenring
from polynom_restklassenring import *


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


'''Berechnung von ggT(a,b) und u,v mit ua + vb = ggT(a,b) '''
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
    '''Benny: normierung habe ich probeweise entfernt'''
    '''a.ring.eins, u // a, v // a'''
    return a , u , v



def _polynom_ext_ggt(self: Polynomring, a: PolynomringElement, b: PolynomringElement):
    if not (isinstance(a, PolynomringElement) and isinstance(b, PolynomringElement)):
        raise TypeError('Argumente nicht vom Typ PolynomringElement')

    if a.ring != self or b.ring != self:
        raise TypeError('PolynomringElement nicht im Polynomring')

    return Polynomring.ExtGGT(a, b)


Polynomring.ExtGGT = staticmethod(_polynom_ExtGGT)
Polynomring.ext_ggt = _polynom_ext_ggt

def _polynom_GGT(a: PolynomringElement, b: PolynomringElement):
    if not (isinstance(a, PolynomringElement) and isinstance(b, PolynomringElement)):
        raise TypeError('Argumente nicht vom Typ PolynomringElement')

    if a.basisring != b.basisring:
        raise ValueError(
            'PolynomringElement haben nicht den gleichen Grundring')
        
    if b==b.ring.null:
        return a
    return _polynom_GGT(b, a % b)

Polynomring.GGT = staticmethod(_polynom_GGT)

def _primes(n):
    divisors = [d for d in range(2, n+1) if n % d == 0]
    return [d for d in divisors if
            all(d % od != 0 for od in divisors if od != d)]


def _polynom_irreduzibel(f: PolynomringElement):
    if not isinstance(f.basisring, Restklassenring):
        raise TypeError('Bassisring muss Restklassenring sein')
    if f.grad==0:
        return False
    
    KX_f = PolynomRestklassenring(f)
    var = PolynomRestklassenringElement(f.ring.variable, KX_f)

    n = [int(f.grad / p) for p in _primes(f.grad)]

    for i in range(0, len(n)):
        h = (((var ** f.basisring.modulus) **  n[i]) - var)
        g = Polynomring.GGT(f, h.wert)
        if g.grad!=0:
            return False

    g = (((var ** f.basisring.modulus) ** f.grad) - var)
    return True


PolynomringElement.irreduzibel = _polynom_irreduzibel
