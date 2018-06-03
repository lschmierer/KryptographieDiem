from tocas import Ganzzahlring, Restklassenring, RestklassenringElement, PolynomringElement

from bruchzahlring import Bruchzahlring


def ganzzahlring_str(self):
    return '\u2124'


Ganzzahlring.__str__ = ganzzahlring_str


def restklassenring_str(self):
    return "\u2124/{0}\u2124".format(self.modulus)


Restklassenring.__str__ = restklassenring_str


def restklassenring_element_str(self):
    return '{} in {}'.format(self.drucke_element(), self.ring)


RestklassenringElement.__str__ = restklassenring_element_str


def polynomring_element_str(self):
    return '{} in {}'.format(self.drucke_element(), self.ring)


PolynomringElement.__str__ = polynomring_element_str
