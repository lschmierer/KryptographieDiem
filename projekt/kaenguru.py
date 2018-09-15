import math

from tocas.AbstrakteRinge import RingElement
from tocas.Restklassenringe import Restklassenring, RestklassenringElement

import projekt.hash_extension
import projekt.zwei_adisch_extension
from projekt.abstrakte_gruppen import AdditiveGruppenElement


def _generiere_walk(g, h, F_r, w, n_s):
    """Generiert die ursprüngliche (originale) Walk Funktion von Pollard."""
    if isinstance(g, RingElement):
        if not isinstance(h, RingElement):
            raise TypeError(
                'Parameter h ist nicht vom selben Typ wie Parameter g')

        def mult(a, b):
            return a * b

        def exp(a, b):
            return a ** b

    elif isinstance(g, AdditiveGruppenElement):
        if not isinstance(h, AdditiveGruppenElement):
            raise TypeError(
                'Parameter h ist nicht vom selben Typ wie Parameter g')

        def mult(a, b):
            return a + b

        def exp(a, b):
            return a * b

    else:
        raise TypeError(
            'Parameter sind nicht vom Typ RingElement oder AdditiveGruppeElement')

    if not isinstance(F_r, Restklassenring):
        raise TypeError('Parameter F_r ist nicht vom Typ  Restklassenring')
    if not isinstance(w, int):
        raise TypeError('Parameter w ist nicht vom Typ  int')
    if not isinstance(n_s, int):
        raise TypeError('Parameter n_s ist nicht vom Typ  int')

    g_pre = []
    for j in range(n_s):
        u = F_r.element(2 ** j)

        g_pre.append((u, exp(g, u.wert)))

    def walk(x, a: RestklassenringElement):
        if not isinstance(x, type(g)):
            raise TypeError(
                'Parameter x ist nicht vom selben Typ wie g')
        if not isinstance(a, RestklassenringElement):
            raise TypeError(
                'Parameter a ist nicht vom Typ  RestklassenringElement')

        S_x = x.zwei_adisch()[0] % n_s

        (u, g_S_x) = g_pre[S_x]

        a += u
        x = mult(x, g_S_x)

        return (x, a)

    return walk


def kaenguru(g, h, r: int, b: int, w: int, n_d: int, n_s=256):
    """Känguru (Lambda) Methode um diskrete Logarithmen zwischen b und b + w zu finden.
    
    h = g ^ a mit r Ordnung von h
    
    Parameter n_d gibt die Anzahl an least-significant bits an
    die null sein müssen, sodass ein Element als distinguished
    Element makiert wird.
    Parameter n_s definiert die Länge des Walks."""
    if isinstance(g, RingElement):
        if not isinstance(h, RingElement):
            raise TypeError(
                'Parameter h ist nicht vom selben Typ wie Parameter g')

        def mult(a, b):
            return a * b

        def exp(a, b):
            return a ** b
    elif isinstance(g, AdditiveGruppenElement):
        if not isinstance(h, AdditiveGruppenElement):
            raise TypeError(
                'Parameter h ist nicht vom selben Typ wie Parameter g')

        def mult(a, b):
            return a + b

        def exp(a, b):
            return a * b
    else:
        raise TypeError(
            'Parameter sind nicht vom Typ RingElement oder AdditiveGruppeElement')
    if not isinstance(r, int):
        raise TypeError('Parameter r ist nicht vom Typ  int')
    if not isinstance(b, int):
        raise TypeError('Parameter b ist nicht vom Typ  int')
    if not isinstance(w, int):
        raise TypeError('Parameter w ist nicht vom Typ  int')
    if not isinstance(n_d, int):
        raise TypeError('Parameter n_d ist nicht vom Typ  int')
    if not isinstance(n_s, int):
        raise TypeError('Parameter n_s ist nicht vom Typ  int')

    h = mult(h, exp(g, -b))

    F_r = Restklassenring(r)

    walk = _generiere_walk(g, h, F_r, w, n_s)

    y_exp = F_r.element(0)
    y = h

    x_exp = F_r.element(math.floor(w / 2))
    x = exp(g, x_exp.wert)

    distinguished_points = {}
    while True:
        (x, x_exp) = walk(x, x_exp)

        # schnelles modulo rechnen für Zweierpotenzen
        if x.zwei_adisch()[0] & ((2 ** n_d) - 1) == 0:
            if x in distinguished_points:
                break
            else:
                distinguished_points[x] = x_exp

        # x und y tauschen (um abwechselnd voran zu schreiten)
        (x, y) = (y, x)
        (x_exp, y_exp) = (y_exp, x_exp)

    y_exp = distinguished_points[x]

    a = x_exp - y_exp
    if exp(g, a.wert) != h:
        a = y_exp - x_exp

    return b + a.wert
