from tocas.AbstrakteRinge import RingElement, Ganzzahlring, RingTupel
from tocas.Restklassenringe import Restklassenring, RestklassenringElement
from tocas.Polynomringe import PolynomringElement

import ha.polynom_extension
import ha.restklassen_extension
from ha.polynom_restklassenring import PolynomRestklassenringElement
import math

from projekt.abstrakte_gruppen import AdditiveGruppenElement
from projekt.weierstrass_kurvengruppe import WeierstrassKurvengruppenElement
from projekt.edwards_kurvengruppe import EdwardsKurvengruppenElement

def babyStepGiantStep(g, h, r: int):
    "Baby-Step-Giant-Step Algorithmus zur Lösung des diskreten Logarithmus-Problems"

    if isinstance(g, RingElement):
        if not isinstance(h, RingElement):
            raise TypeError(
                'Parameter h ist nicht vom selben Typ wie Parameter g')
        if g.ring != h.ring:
            raise ValueError('g und h sind nicht im selben Ring')

        def mult(a, b):
            return a * b
            
        def exp(a, b):
            return a ** b
        
        def neutral(a):
            return a.ring.eins

    elif isinstance(g, AdditiveGruppenElement):
        if not isinstance(h, AdditiveGruppenElement):
            raise TypeError(
                'Parameter h ist nicht vom selben Typ wie Parameter g')
        if g.gruppe != h.gruppe:
            raise ValueError('g und h sind nicht zur selben Gruppe')

        def mult(a, b):
            return a + b
            
        def exp(a, b):
            return a * b
        
        def neutral(a):
            return a.gruppe.neutral

    else:
        raise TypeError(
            'Parameter sind nicht vom Typ RingElement oder AdditiveGruppeElement')

    m = math.ceil(math.sqrt(r))
    hashtable = dict()
    x = neutral(g)
    for i in range(0,m+1):
        hashtable[x]=i
        x=mult(g,x)
    u = exp(g,-m)
    y, j = h, 0
    while(hashtable.get(y) is None):
        y=mult(y,u)
        j+=1
    i = hashtable.get(y)
    if(i is not None):
        return i + m * j
    else:
        raise ValueError('h kann nicht aus g erzeugt werden') 
            
        
    
def _hash_RestklassenringElement(self):
    return hash(self.wert)
    
def _hash_PolynomRestklassenringElement(self):
    return hash(self.wert)    
    
def _hash_PolynomringElement(self):
    return hash(self.koeffizienten)
    
def _hash_RingTupel(self):
    return hash((self.laenge, tuple(self.koeffizienten)))
    
def _hash_WeierstrassKurvengruppenElement(self):
    return hash((self.x, self.y))
    
def _hash_EdwardsKurvengruppenElement(self):
    return hash((self.x, self.y))
    
    
PolynomRestklassenringElement.__hash__ = _hash_PolynomRestklassenringElement
PolynomringElement.__hash__ = _hash_PolynomringElement
RingTupel.__hash__ = _hash_RingTupel
RestklassenringElement.__hash__ =  _hash_RestklassenringElement
WeierstrassKurvengruppenElement.__hash__ = _hash_WeierstrassKurvengruppenElement
EdwardsKurvengruppenElement.__hash__ = _hash_EdwardsKurvengruppenElement
