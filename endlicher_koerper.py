import math

from tocas import Restklassenring, Polynomring, PolynomringElement

import polynom_extension
import prime
from polynom_restklassenring import PolynomRestklassenring


def EndlicherKoerper(p, n=None, prime_test=prime.miller_rabin):
    if not n:
        q = p

        for i in range(2, q // 2 + 1):
            n = math.log(q, i)
            if n.is_integer() and prime_test(i):
                n = int(n)
                p = i
                break
        else:
            raise TypeError(
                'Erstes Argument muss Primzahl oder Primpotenz sein')
    elif not prime_test(p):
        raise TypeError('p ist keine Primzahl')
    elif n < 1:
        raise TypeError('n ist keine ganze Zahl')

    R = Restklassenring(p)

    if n == 1:
        return R

    RX = Polynomring(R)

    koeffizienten = [0] * n
    koeffizienten[-1] = 1

    index = 0
    while index < len(koeffizienten):
        f = PolynomringElement(koeffizienten, RX)
        if f.irreduzibel():
            return PolynomRestklassenring(f)

        if koeffizienten[index] == p - 1:
            index += 1
        else:
            koeffizienten[index] += 1
