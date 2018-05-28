from tocas import Ring, RingElement, PolynomringElement

import polynom_extension


class PolynomRestklassenring(Ring):
    def __init__(self, f: PolynomringElement):
        if not isinstance(f, PolynomringElement):
            raise RuntimeError("Das angegebene Objekt ist kein Polynom.")

        self.modulus = f
        self.null = f.ring.null
        self.eins = f.ring.eins

        self._frier()

    def __str__(self):
        return "{}/({})".format(self.modulus.basisring, self.modulus)

    def __eq__(self, other):
        if not super().__eq__(other):
            return False
        return (self.modulus == other.modulus)

    def element(self, a):
        return PolynomRestklassenringElement(a, self)


class PolynomRestklassenringElement(RingElement):
    def __init__(self, p, r: PolynomRestklassenring):
        if p.basisring != r.modulus.basisring:
            raise RuntimeError("Polynom und Ring nicht vom selben Basisring.")

        self.ring = r

        if isinstance(p, PolynomRestklassenringElement):
            if p.ring.modulus % self.ring.modulus == 0:
                self.wert = p.wert % self.ring.modulus

            else:
                raise RuntimeError("Die Moduli passen nicht zusammen.")

        else:
            if not isinstance(p, PolynomringElement):
                p = PolynomringElement(p, r.modulus.ring)

            self.wert = p % self.ring.modulus

    def drucke_element(self):
        return "[{0}]_{1}".format(self.wert, self.ring.modulus)

    def __neg__(self):
        return PolynomRestklassenringElement(-self.wert, self.ring)

    def __add__(self, other):
        super().__add__(other)
        return PolynomRestklassenringElement(self.wert+other.wert, self.ring)

    def __rmul__(self, other):
        super().__rmul__(other)

        if not isinstance(other, PolynomRestklassenringElement):
            raise RuntimeError(
                "Das Element is kein PolynomRestklassenElement.")

        # TODO https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication#Double-and-add 


        