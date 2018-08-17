from tocas.AbstrakteRinge import Ganzzahlring
from tocas.Restklassenringe import Restklassenring

import projekt.zwei_adisch_extension

def rho_faktorisieren(N, f=lambda x: x ** 2 + x.ring.element(1)):
    """Pollards Rho Methode zum Faktorisieren."""
    if not isinstance(N, int):
        raise TypeError(
            'Primfaktorzerlegung nur für Ganzzahlen')

    F_N = Restklassenring(N)
    x_1 = F_N.element(2)
    x_2 = f(x_1)

    while True:
        x_1 = f(x_1)
        x_2 = f(f(x_2))
        d = Ganzzahlring.ExtGGT(((x_2 - x_1).wert), N)[0]

        if d > 1 and d < N:
            break

    return d
