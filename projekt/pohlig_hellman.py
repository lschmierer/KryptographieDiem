from tocas.AbstrakteRinge import RingElement, Ganzzahlring
from tocas.Restklassenringe import Restklassenring

from projekt.abstrakte_gruppen import AdditiveGruppenElement


def pohlig_hellman(g, h, l):
    """Pohlig Hellman Algirthmus für das diskrete Logarithmus Problem.

    h = g ^ a
    l = [(li, ei)] Faktorisierung der Gruppenordnung N (von g)
    """

    if isinstance(g, RingElement):
        if not isinstance(h, RingElement):
            raise TypeError(
                'Parameter h ist nicht vom selben Typ wie Parameter g')
        if g.ring != h.ring:
            raise ValueError('g und h sind nicht im selben Ring')

        def mult(a, b):
            return a * b

        def exp(a, b):
            return a ** b

        def neutral(a):
            return a.ring.eins

    elif isinstance(g, AdditiveGruppenElement):
        if not isinstance(h, AdditiveGruppenElement):
            raise TypeError(
                'Parameter h ist nicht vom selben Typ wie Parameter g')
        if g.gruppe != h.gruppe:
            raise ValueError('g und h sind nicht zur selben Gruppe')

        def mult(a, b):
            return a + b

        def exp(a, b):
            return a * b

        def neutral(a):
            return a.gruppe.neutral

    else:
        raise TypeError(
            'Parameter sind nicht vom Typ RingElement oder AdditiveGruppeElement')

    if not isinstance(l, list):
        raise TypeError('Parameter l ist keine Liste')
    for t in l:
        if not isinstance(t, tuple) or len(t) != 2:
            raise TypeError(
                'Element von l ist kein Tupel oder kein Tupel der Länge 2')
        if not isinstance(t[0], int) or t[0] < 0:
            raise TypeError('Prim {} ist keine natürliche Zahl'.format(t[0]))
        if not isinstance(t[1], int) or t[1] < 0:
            raise TypeError(
                'Primfaktor {} ist keine natürliche Zahl'.format(t[1]))

    N = 1
    for t in l:
        N *= t[0] ** t[1]

    # Compute {g^(N/l_i^f_i), h^(N/l_i^f_i) : 1 <= i <= n, 1 <=f <= e_i}
    gNl = []
    hNl = []
    for i in range(len(l)):
        gNl.append([])
        hNl.append([])
        for f_i in range(1, l[i][1] + 1):
            gNl[i].append(exp(g, N // l[i][0] ** f_i))
            hNl[i].append(exp(h, N // l[i][0] ** f_i))

    a = []

    for i in range(len(l)):
        a.append(0)

        for j in range(l[i][1]):
            g_0 = gNl[i][j]
            h_0 = hNl[i][j]

            # Compute u = g^(−a_i) and h_0 = h_0 * u
            u = exp(g_0, -a[i])
            h_0 = mult(h_0, u)

            if h_0 != neutral(h):
                g_0 = gNl[i][0]

                b = 1
                T = g_0

                while h_0 != T:
                    b = b + 1
                    T = mult(T, g_0)

                a[i] = a[i] + b * l[i][0] ** j

    a_res = 0

    # Chinesicher Restsatz
    for i in range(len(l)):
        N_i = l[i][0] ** l[i][1]
        M_i = N // N_i
        a_res += M_i * a[i] * Ganzzahlring.ExtGGT(M_i, N_i)[1]

    return a_res % N
