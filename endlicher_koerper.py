import math
import random
import decimal

from tocas import Restklassenring, Polynomring, PolynomringElement, Ring

import polynom_extension
import prime
import restklassen_extension
from polynom_restklassenring import PolynomRestklassenring


def EndlicherKoerper(p, n=None, prime_test=prime.miller_rabin, variablenname = "x"):
    if isinstance(p, Ring):
        if p.ist_endlicher_koerper():
             R=p
        else:
            raise TypeError(
                'Erstes Argument muss ein endlicher Körper sein')
    else:
        if not n:
            q = p
            for exp in range(2, int(math.log(q,2)) +1):
                basis = decimal.Decimal(q) ** (decimal.Decimal(1)/decimal.Decimal(exp))
                if basis % 1 == 0 and prime_test(int(basis)):
                    p=int(basis)
                    n=exp
                    break
            else:
                if prime_test(p):
                    n = 1
                else:
                    raise TypeError(
                        'Erstes Argument muss Primzahl oder Primpotenz sein')
        elif not prime_test(p):
            raise TypeError('p ist keine Primzahl')
        R = Restklassenring(p)
    if n < 1:
        raise TypeError('n ist keine natürliche Zahl')

    if n == 1:
        return R

    RX = Polynomring(R, variablenname = variablenname)

    koeffizienten = [RX.basisring.null] * (n + 1)

    random.seed(0)
    while True:
        '''for i in range(0, n): '''
        '''    koeffizienten[i] += random.randint(0, R.modulus-1) '''
        '''    koeffizienten[i] %= R.modulus '''
        
        koeffizienten[random.randint(0,n)] += RX.basisring.eins
        if isinstance(R, PolynomRestklassenring):
            koeffizienten[random.randint(0,n)] += R.erzeuger
        
        if koeffizienten[-1] == RX.basisring.null:
            koeffizienten[-1] += RX.basisring.eins
        
        f = PolynomringElement(koeffizienten, RX)
        if f.irreduzibel():
            return PolynomRestklassenring(f)
