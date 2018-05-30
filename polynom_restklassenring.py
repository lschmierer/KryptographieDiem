from tocas import Ring, RingElement, PolynomringElement, RingTupel

import polynom_extension


class PolynomRestklassenring(Ring):
    def __init__(self, f: PolynomringElement):
        if not isinstance(f, PolynomringElement):
            raise RuntimeError("Das angegebene Objekt ist kein Polynom.")

        self.modulus = f
        self.null = PolynomRestklassenringElement(f.ring.null, self)
        self.eins = PolynomRestklassenringElement(f.ring.eins, self)

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
        self.ring = r

        if isinstance(p, PolynomRestklassenringElement):
            if p.basisring != r.modulus.basisring:
                raise RuntimeError(
                    "Polynom und Ring nicht vom selben Basisring.")

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

    def __eq__(self, other):
        if not super().__eq__(other):
            return False
        return self.wert == other.wert

    def __neg__(self):
        return PolynomRestklassenringElement(-self.wert, self.ring)

    def __add__(self, other):
        super().__add__(other)
        return PolynomRestklassenringElement(self.wert+other.wert, self.ring)

    def __rmul__(self, other):
        super().__rmul__(other)

        if type(other) == int:
            return PolynomRestklassenringElement(RingElement.intmult(other, self.wert), self.ring)

        if not isinstance(other, RingElement):
            raise TypeError(
                "Der erste Faktor ist keine Zahl und kein Ringelement.")

        if other.ring == self.ring.modulus.basisring:
            return PolynomRestklassenringElement(other*self.wert.koeffizienten, self.ring)

        if self == self.ring.null or other == self.ring.null:
            return self.ring.null

        r = PolynomRestklassenringElement((self.wert.grad + 1)*[self.wert.basisring.null], self.ring)

        for d in range(other.wert.grad, 0, -1):
            r += other.wert.koeffizient(d) * self
            r = PolynomRestklassenringElement(RingTupel([r.wert.basisring.null] + r.wert.koeffizienten.koeffizienten), self.ring)
        
        r += other.wert.koeffizient(0) * self

        return r

    def invers(self):
        pass
