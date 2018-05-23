from tocas.AbstrakteRinge import Ring, RingElement, Ganzzahlring


class Bruchzahlring(Ring):
    """Ring der rationalen Zahlen"""

    def __init__(self):
        self.null = BruchzahlringElement(0, 1, self)
        self.eins = BruchzahlringElement(1, 1, self)

        self._frier()

    def __str__(self):
        return "Q"

    def __eq__(self, other):
        return super().__eq__(other)

#Vorschlag Benny:
    def element(self, p, q):
        if not (isinstance(p,int) & isinstance(q,int)) :
            raise TypeError("Elemente sind keine ganzen Zahlen.")
        return BruchzahlringElement(p,q, self)

# alte Version (kann nur ganze Zahlen)
#    def element(self, e):
#        if not type(e) == int:
#            raise TypeError("Element ist keine ganze Zahl.")
#        return BruchzahlringElement(e, 1, self)


Q = Bruchzahlring


class BruchzahlringElement(RingElement):
    """Rationalen Zahl"""

    def __init__(self, a, b, ring=None):
        if not (isinstance(a, int) and isinstance(b, int)):
            raise TypeError(
                "Die angegebenen Parameter sind keine ganzen Zahlen.")

        ggt = Ganzzahlring.ExtGGT(a, b)[0]

        self.a = a // ggt
        self.b = b // ggt
        if not ring:
            ring = Bruchzahlring()
        self.ring = ring

    def drucke_element(self):
        return '{}/{}'.format(self.a, self.b)

    def __str__(self):
        return self.drucke_element() + "  in " + self.ring.__str__()

    def __eq__(self, other):
        if not super().__eq__(other):
            return False
        return self.a == other.a and self.b == other.b

    def __neg__(self):
        return BruchzahlringElement(-self.a, self.b, self.ring)

    def __add__(self, other):
        super().__add__(other) #?
        if type(other) == int:
            return BruchzahlringElement(self.a + other * self.b, self.b, self.ring)
        elif isinstance(other, BruchzahlringElement):
            return BruchzahlringElement(self.a * other.b + other.a * self.b, self.b * other.b, self.ring)

    def __rmul__(self, other):
        super().__rmul__(other) #?
        if type(other) == int:
            return BruchzahlringElement(self.a * other, self.b, self.ring)
        elif isinstance(other, BruchzahlringElement):
            return BruchzahlringElement(self.a * other.a, self.b * other.b, self.ring)

    def invers(self):
        return BruchzahlringElement(self.b, self.a, self.ring)
