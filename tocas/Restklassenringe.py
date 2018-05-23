from .AbstrakteRinge import *

# Zufall:

from random import randint

#----------------------------------------------------
# Instanziierbare Klasse Restklassenring


class Restklassenring(Ring):

    def __init__(self,n : int):
    
        if not isinstance(n,int):
            raise RuntimeError("Das angegebene Objekt ist keine ganze Zahl.")
        if n <= 0:
            raise RuntimeError("Der Modulus ist nicht positiv.")
        self.modulus = n
        self.null = RestklassenringElement(0,self)
        self.eins = RestklassenringElement(1,self)

        self._frier()

    def __str__(self):
        
        return "Z/{0}Z".format(self.modulus)
    
        
    def __eq__(self,other):
        
        if not super().__eq__(other):
            return False
        return (self.modulus == other.modulus)


    def element(self,a):
        return RestklassenringElement(a,self)


    def random(self):
        
        return RestklassenringElement(randint(0,self.modulus-1),self.modulus)

    

#---------------------------------------------------
# Instanziierbare Klasse RestklassenringElement

class RestklassenringElement(RingElement):
 
 
    
    def __init__(self,a,n):
        
        if isinstance(n,int):
            if n <= 0:
                raise RuntimeError("Der Modulus ist nicht positiv.")
            self.ring = Restklassenring(n)

        elif isinstance(n,Restklassenring):
            self.ring = n

        else:
            raise RuntimeError("Das zweite angegebene Objekt ist keine Zahl und kein Restklassenring.")

        if type(a) == int:

            self.wert = a % self.ring.modulus

        elif type(a) == RestklassenringElement:

            if a.ring.modulus % self.ring.modulus == 0:
                self.wert = a.wert % self.ring.modulus

            else:
                raise RuntimeError("Die Moduli passen nicht zusammen.")

        else:
            raise RuntimeError("Das erste angegebene Objekt ist keine Zahl und kein Restklassenringelement.")

        self._frier()


    def drucke_element(self):

        return "[{0}]_{1}".format(self.wert,self.ring.modulus)


    def __str__(self):
        
        return self.drucke_element() + "  in " + self.ring.__str__()


    def __eq__(self,other):

        if not super().__eq__(other):
            return False
        return self.wert == other.wert

    

    # Jetzt kommt das Überladen / Definieren der arithmetischen Operatoren

    
    def __neg__(self):

        return RestklassenringElement(-self.wert, self.ring)


    def __add__(self,other):
        
        super().__add__(other)
        return RestklassenringElement(self.wert+other.wert,self.ring)

        

    def __rmul__(self,other):
 
        super().__rmul__(other)

        # Der eine Faktor ist a:
        # Dieser Faktor ist ein Ringelement:
        
        a = self
                
        # Der andere Faktor ist b
        # Die Eingabe ist ja: other*self
        # Die Bedingung lautet: other muss entweder eine Zahl sein
        # oder ein Restklassenringelement, dessen modulus
        # ein Vielfaches von dem von a ist:
        # Dieser Faktor wird (zunächst) als Zahl dargestellt. 

        if type(other) == int:
            b = other
        elif (isinstance(other,RestklassenringElement) and 
                            other.ring.modulus % self.ring.modulus == 0):
            b = other.wert % self.ring.modulus
        else:
            raise RuntimeError("Die Elemente können nicht multipliziert werden.")
 
        # Umwandlung in 2-adische Schreibweise:
        
        zweiadisch = ZweiAdisch(b)

        # Jetzt kommt double-and-add


        c = self.ring.null

        for i in range (0,len(zweiadisch)-1):
            if zweiadisch[i] == '1':
                c = c + a
            c = c + c

        # Am Ende muss man noch einmal addieren, ohne zu multiplizieren.
     
        if (len(zweiadisch) > 0 
                and zweiadisch[len(zweiadisch)-1] == '1'):
            c = c + a

        return c



    def invers(self):

        a = self.wert
        b = self.ring.modulus

        u, s = RestklassenringElement(1,self.ring), RestklassenringElement(0,self.ring)

        # Sehr kompakte GGT-Modulo-Berechnung
        while b!=0:
            q=a//b
            a, b = b, a-q*b
            u, s = s, u-q*s

        if a != 1:
            raise InvertierungsFehler(self)

        return u

