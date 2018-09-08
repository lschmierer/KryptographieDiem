from tocas.AbstrakteRinge import Ring, RingElement, ZweiAdisch

import ha.polynom_extension
import ha.restklassen_extension

from projekt.abstrakte_gruppen import AdditiveGruppe, AdditiveGruppenElement


class EdwardsKurvengruppe(AdditiveGruppe):
    """Ring der eliptischen Kurven in Edwards Darstellung"""

    def __init__(self, ring: Ring, d: RingElement):
        if not isinstance(ring, Ring):
            raise TypeError('Parameter ring ist nicht vom Typ Ring')
        if not isinstance(d, RingElement):
            raise TypeError('Parameter d ist nicht vom Typ RingElement')
        if d.ring != ring:
            raise ValueError('d ist nicht im Ring r')

        self.basisring = ring
        self.d = d

        self.neutral = EdwardsKurvengruppenElement(ring.null, ring.eins, self)

        self._frier()

    def __str__(self):
        return 'EdwardsKurvengruppe(ring={}, d={})'.format(self.basisring, self.d)

    def __eq__(self, other):
        return super().__eq__(other)

    def element(self, x, y):
        if isinstance(x, EdwardsKurvengruppenElement):
            return x

        if not (isinstance(x, self.basisring) and isinstance(y, self.basisring)):
            raise TypeError(
                'Elemente sind nicht im Basisring {}'.format(self.basisring))
        return EdwardsKurvengruppenElement(x, y, self)

    def ist_endlich(self):
        return self.basisring.ist_endlicher_koerper()

    def __hash__(self):
        return hash((self.basisring, self.d))


class EdwardsKurvengruppenElement(AdditiveGruppenElement):
    """Punkt auf einer elliptischen Kurve in Edwards Darstellung."""

    def __init__(self, x: RingElement, y: RingElement, gruppe: EdwardsKurvengruppe):
        if not isinstance(gruppe, EdwardsKurvengruppe):
            raise TypeError(
                'Parameter gruppe ist nicht vom Typ EdwardsKurvengruppe')
        if not (isinstance(x, RingElement) and isinstance(y, RingElement)):
            raise TypeError(
                'Die angegebenen Parameter sind keine Ring Elemente')
        if not (x.ring == gruppe.basisring and y.ring == gruppe.basisring):
            raise ValueError(
                'Die angegebenen Elemente sind nicht im Ring {}'.format(gruppe.basisring))

        self.gruppe = gruppe
        self.x = x
        self.y = y

        self._frier()

    def __str__(self):
        return '{} in {}'.format(self.drucke_element(), self.gruppe)

    def drucke_element(self):
        return '({}, {})'.format(self.x, self.y)

    def drucke_element_mit_klammern(self):
        return self.drucke_element()

    def __eq__(self, other):
        if not super().__eq__(other):
            return False
        return self.x == other.x and self.y == other.y

    def __neg__(self):
        return EdwardsKurvengruppenElement(-self.x, self.y, self.gruppe)

    def __add__(self, other):
        if not isinstance(other, EdwardsKurvengruppenElement):
            raise TypeError(
                'Element nicht vom selben Typ (EdwardsKurvengruppenElement)')
        if self.gruppe != other.gruppe:
            raise TypeError('Elemente nicht in der selben Gruppe')

        x1, y1 = self.x, self.y
        x2, y2 = other.x, other.y

        return EdwardsKurvengruppenElement(
            (x1 * y2 + x2 * y1) / (self.gruppe.basisring.eins +
                                   self.gruppe.d * x1 * x2 * y1 * y2),
            (y1 * y2 - x1 * x2) / (self.gruppe.basisring.eins - self.gruppe.d * x1 * x2 * y1 * y2), self.gruppe)

    def __mul__(self, other):
        super().__mul__(other)

        if (other < 0):
            other = -other
            self = -self

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

    def zwei_adisch(self):
        (zwei_adisch, laenge) = self.x.zwei_adisch()
        zwei_adisch <<= laenge
        (w, l) = self.y.zwei_adisch()
        zwei_adisch += w
        laenge += l
        return (zwei_adisch, laenge)

    def __hash__(self):
        return hash((self.x, self.y, self.gruppe))
