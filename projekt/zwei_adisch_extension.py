import math

from tocas.AbstrakteRinge import RingTupel
from tocas.Restklassenringe import RestklassenringElement
from tocas.Polynomringe import PolynomringElement

from ha.polynom_restklassenring import PolynomRestklassenringElement

import projekt.hash_extension
from projekt.abstrakte_gruppen import AdditiveGruppenElement


def _ring_tupel_zwei_adisch(self):
    zwei_adisch = 0
    laenge = 0
    for k in self.koeffizienten:
        (w, l) = k.zwei_adisch()
        if laenge > 0:
            zwei_adisch <<= l
        zwei_adisch += w
        laenge += l
    return (zwei_adisch, laenge)


def _restklassenring_element_zwei_adisch(self):
    return (self.wert, self.ring.modulus.bit_length())


def _polynomring_element_zwei_adisch(self):
    return self.koeffizienten.zwei_adisch()


def _polynom_restklassenring_element_zwei_adisch(self):
    return (self.wert.zwei_adisch()[0], self.ring.modulus.zwei_adisch()[1])


RingTupel.zwei_adisch = _ring_tupel_zwei_adisch
RestklassenringElement.zwei_adisch = _restklassenring_element_zwei_adisch
PolynomringElement.zwei_adisch = _polynomring_element_zwei_adisch
PolynomRestklassenringElement.zwei_adisch = _polynom_restklassenring_element_zwei_adisch