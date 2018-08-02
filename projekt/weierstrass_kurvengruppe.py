from tocas.AbstrakterAnfang import UnveraenderbaresObjekt
from tocas.AbstrakteRinge import Ring, RingElement, ZweiAdisch

import ha.polynom_extension
import ha.restklassen_extension

from projekt.abstrakte_gruppe import Gruppe, GruppenElement


class WeierstrassKurvengruppe(Gruppe):
    """Ring der eliptischen Kurven in (kurzer) Weierstrass Darstellung"""

    def __init__(self, ring: Ring, a: RingElement, b: RingElement):
        if not isinstance(ring, Ring):
            raise TypeError('Parameter ring ist nicht vom Typ Ring')
        if not isinstance(a, RingElement):
            raise TypeError('Parameter a ist nicht vom Typ RingElement')
        if not isinstance(b, RingElement):
            raise TypeError('Parameter b ist nicht vom Typ RingElement')
        if a.ring != ring:
            raise ValueError('a ist nicht im Ring r')
        if a.ring != ring:
            raise ValueError('b ist nicht im Ring r')

        self.basisring = ring
        self.a = a
        self.b = b

        self.neutral = WeierstrassKurvengruppenElement(
            ring.eins, ring.eins, self, isPointAtInfinity=True)

        self._frier()

    def __str__(self):
        return 'WeierstrassKurvengruppe(ring={}, a={}, b={})'.format(self.basisring, self.a, self.b)

    def __eq__(self, other):
        return super().__eq__(other)

    def element(self, x, y):
        if isinstance(x, WeierstrassKurvengruppenElement):
            return x

        if not (isinstance(x, self.basisring) and isinstance(y, self.basisring)):
            raise TypeError(
                'Elemente sind nicht im Basisring {}'.format(self.basisring))
        return WeierstrassKurvengruppenElement(x, y, self)

    def ist_endlich(self):
        return self.basisring.ist_endlicher_koerper()


class WeierstrassKurvengruppenElement(GruppenElement):
    """Punkt auf einer elliptischen Kurve in (kurzer) Weierstrass Darstellung."""

    def __init__(self, x: RingElement, y: RingElement, gruppe: WeierstrassKurvengruppe, isPointAtInfinity=False):
        if not isinstance(gruppe, WeierstrassKurvengruppe):
            raise TypeError(
                'Parameter gruppe ist nicht vom Typ WeierstrassKurvengruppe')
        if not (isinstance(x, RingElement) and isinstance(y, RingElement)):
            raise TypeError(
                'Die angegebenen Parameter sind keine Ring Elemente')
        if not (x.ring == gruppe.basisring and y.ring == gruppe.basisring):
            raise ValueError(
                'Die angegebenen Elemente sind nicht im Ring {}'.format(gruppe.basisring))

        self.gruppe = gruppe
        self.x = x
        self.y = y
        self.isPointAtInfinity = isPointAtInfinity

        self._frier()

    def __str__(self):
        return '{} in {}'.format(self.drucke_element(), self.gruppe)

    def drucke_element(self):
        if self.isPointAtInfinity:
            return '(Point_At_Infinity)'
        return '({}, {})'.format(self.x, self.y)

    def drucke_element_mit_klammern(self):
        return self.drucke_element()

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        if self.gruppe != other.gruppe:
            return False
        return self.x == other.x and self.y == other.y

    def __neg__(self):
        return WeierstrassKurvengruppenElement(self.x, -self.y, self.gruppe)

    def __add__(self, other):
        if not isinstance(other, WeierstrassKurvengruppenElement):
            raise TypeError(
                'Element nicht vom selben Typ (WeierstrassKurvengruppenElement)')
        if self.gruppe != other.gruppe:
            raise TypeError('Elemente nicht in der selben Gruppe')

        if self.isPointAtInfinity:
            return other

        if other.isPointAtInfinity:
            return self

        x1, y1 = self.x, self.y
        x2, y2 = other.x, other.y

        if x1 == x2:
            if y1 == y2:
                return self.double()
            else:
                return self.gruppe.neutral

        s = (y1 - y2) / (x1 - x2)
        newX = (s**2) - x1 - x2
        return WeierstrassKurvengruppenElement(newX,
                                               s*(x1 - newX) - y1,
                                               self.gruppe)

    def __mul__(self, other):
        super().__mul__(other)

        zweiadisch = ZweiAdisch(other)

        res = self.gruppe.neutral
        for i in range(0, len(zweiadisch)-1):
            if zweiadisch[i] == '1':
                res = res + self
            res = res + res

        # Am Ende muss man noch einmal addieren, ohne zu multiplizieren.
        if (len(zweiadisch) > 0
                and zweiadisch[len(zweiadisch)-1] == '1'):
            res = res + self

        return res

    def double(self):
        if self.isPointAtInfinity:
            return self
        if self.y == self.y.ring.null:
            return self
        s = (3 * (self.x**2) + self.gruppe.a) / (2 * self.y)
        newX = s**2 - 2 * self.x
        return WeierstrassKurvengruppenElement(newX,
                                               s * (self.x - newX) - self.y,
                                               self.gruppe)
