import random
import math

from tocas import Ganzzahlring, Polynomring, Restklassenring

import ha.polynom_extension


def miller_rabin(n, k=40):
    if not isinstance(n, int):
        raise TypeError('Argumente nicht vom Typ int')

    if n <= 1:
        return False

    if n == 2:
        return True
    if n % 2 == 0:
        return False

    s = 0
    t = n - 1
    while t % 2 == 0:
        s += 1
        t //= 2

    ZnZ = Restklassenring(n)

    for _ in range(k):
        a = ZnZ.element(random.randrange(1, n - 1))
        a = a ** t

        if a == ZnZ.eins:
            continue
        for _ in range(s):
            if a == -ZnZ.eins:
                break
            elif a == ZnZ.eins:
                return False

            a = a ** 2
        else:
            return False

    return True


def _ord(r, n):
    if Ganzzahlring.ExtGGT(r, n)[0] > 1:
        return math.inf

    ZrZ = Restklassenring(r)

    k = 1
    while ZrZ.element(n) ** k != ZrZ.eins:
        k += 1

    return k


def _phi(r):
    phi = 0

    for i in range(1, r):
        if Ganzzahlring.ExtGGT(r, i)[0] == 1:
            phi += 1

    return phi


def aks(n):
    from ha.polynom_restklassenring import PolynomRestklassenring

    if not isinstance(n, int):
        raise TypeError('Argumente nicht vom Typ int')

    if n <= 1:
        return False

    for a in range(2, math.ceil(math.sqrt(n))):
        b = 2
        while a ** b <= n:
            if n == a ** b:
                return False
            b += 1

    r = 1
    while _ord(r, n) <= math.log2(n) ** 2:
        r += 1

    for a in range(2, r + 1):
        ggt = Ganzzahlring.ExtGGT(a, n)[0]

        if ggt > 1 and ggt < n:
            return False

    if n <= r:
        return True

    K_X_n = Polynomring(Restklassenring(n))
    K_X_n_f = PolynomRestklassenring(K_X_n.variable ** r - K_X_n.eins)

    for a in range(1, math.floor(math.sqrt(_phi(r)) * math.log2(n) + 1)):
        if K_X_n_f.element([a, 1]) ** n != K_X_n_f.erzeuger ** n + K_X_n_f.element([a]):
            return False

    return True
