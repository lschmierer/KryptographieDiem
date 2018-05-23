from tocas.AbstrakteRinge import *
from tocas.Restklassenringe import *
from tocas.Polynomringe import *
from tocas.Homomorphismen import *



# Zufall:

from random import randint

#----------------------------------------------------
# Instanziierbare Klasse Bruchzahlring

class Bruchzahlring(Ring):
    def __init__(self):
        self.null = BruchzahlringElement(0,1, self)
        self.eins = BruchzahlringElement(1,1, self)
        self._frier()

    def __str__(self):
        return "Q"
    
    
    def __eq__(self,other):
        return super().__eq__(other)

    def element(self, p, q):
        return BruchzahlringElement(p,q)
    
    
    def random(self, maxZaehler, maxNenner):
        return BruchzahlringElement(randint(0,maxZaehler), randint(1,maxNenner))


#----------------------------------------------------
# Instanziierbare Klasse BruchzahlringElement

class BruchzahlringElement(RingElement):
    def __init__(self,p,q, *theRing):
        if isinstance(p,int) & isinstance(q,int):
            if q==0:
                raise RuntimeError("Der Nenner ist gleich 0.")
            else:
                ggt,_,_= Ganzzahlring.ExtGGT(p,q)
                self.zaehler = p//ggt
                self.nenner = q//ggt
                if theRing is None:
                    self.ring = Bruchzahlring()
                else:
                    self.ring = theRing
        else:
                raise RuntimeError("Das zweite (Zaehler) und dritte (Nenner) Objekt sind nicht vom Typ Integer.")
        
    
    
    def __str__(self):
        return self.drucke_element() + "  in " + self.ring.__str__()

    def drucke_element(self):
        return "{0}/{1}".format(self.zaehler,self.nenner)

    def __eq__(self,other):
    
        if not super().__eq__(other):
            return False
        return self.nenner == other.nenner & self.zaehler == other.zaehler

    def __neg__(self):
        return BruchzahlringElement(-self.zaehler, self.nenner)
    
    
    def __add__(self,other):
        return BruchzahlringElement(self.zaehler*other.nenner + self.nenner*other.zaehler,
                                    self.nenner*other.nenner)

    
    def __rmul__(self,other):
        return BruchzahlringElement(self.zaehler*other.zaehler,self.nenner*other.nenner)

    def invers(self):
        return BruchzahlringElement(self.nenner, self.zaehler)

Q = Bruchzahlring()
