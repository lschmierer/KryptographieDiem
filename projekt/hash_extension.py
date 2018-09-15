from tocas.AbstrakteRinge import RingElement, Ganzzahlring, RingTupel
from tocas.Restklassenringe import Restklassenring, RestklassenringElement
from tocas.Polynomringe import Polynomring, PolynomringElement

from ha.polynom_restklassenring import PolynomRestklassenring, PolynomRestklassenringElement

"""hash() Implementierungen für alle gegebenen Ringe und RingElemente."""


def _ring_tupel_hash(self):
    return hash((self.laenge, tuple(self.koeffizienten)))


def _restklassenring_hash(self):
    return hash(self.modulus)


def _restklassenring_element_hash(self):
    return hash((self.wert, self.ring))


def _polynomring_hash(self):
    return hash(self.basisring)


def _polynomring_element_hash(self):
    return hash((self.koeffizienten, self.ring))


def _polynom_restklassenring_hash(self):
    return hash(self.modulus)


def _polynom_restklassenring_element_hash(self):
    return hash((self.wert, self.ring))


RingTupel.__hash__ = _ring_tupel_hash
Restklassenring.__hash__ = _restklassenring_hash
RestklassenringElement.__hash__ = _restklassenring_element_hash
Polynomring.__hash__ = _polynomring_hash
PolynomringElement.__hash__ = _polynomring_element_hash
PolynomRestklassenring.__hash__ = _polynom_restklassenring_hash
PolynomRestklassenringElement.__hash__ = _polynom_restklassenring_element_hash
