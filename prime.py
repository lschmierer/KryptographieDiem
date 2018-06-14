import random

from tocas import Restklassenring


def miller_rabin(n, k=40):
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
