from .AbstrakterAnfang import *
from copy import deepcopy


# Es werden abstrakte Klassen "Ring" und 
# "RingElement" definiert.
# Die Eingaben werden oftmals nur angegeben, um die Idee
# klarzumachen.
# Dies wird dann in Unterklassen überschrieben.

# Man beachte:
# Eine Klasse mit einer als "abstactmethod" (@abstractmethod) deklarierten
# Methode kann nicht instanziiert werden.
# Aber so eine Methode kann trotzdem mit super(). .. von einer
# Unterklasse aus aufgerufen werden.

# Hiernach wird dann noch die instanziierbare Klassen Ganzzahlring
# und RingTupel definiert.


#-------------------------------------------------------
# Abstrakte Klasse Ring


class Ring(UnveraenderbaresObjekt):
    
    @abstractmethod
    def __init__(self,info):
        
        Ring.null, Ring.eins = None, None
      

    # Das ist ein sehr rudimentärer Gleichheitstest.
    # Der reicht dann nur bei Ganzzahlring aus.

    def __eq__(self,other):

        if not type(self) == type(other):
            return False

        return True


    # Für einen Ring R soll mit R.element(info)
    # eine durch info definierte Instanz der 
    # entsprechenden von RingElement abgeleiteten Klasse
    # zurückgegeben werden.
    # Siehe z.B. in Restklassenring.
 
    @abstractmethod
    def element(self,*info):
        pass

    
    def tupel(self,*koeffizienten):

        return RingTupel(*(koeffizienten+(self,)))
    

#-------------------------------------------------------
# Abstrakte Klasse RingElement

    
class RingElement(UnveraenderbaresObjekt):

    @abstractmethod
    def __init__(self,elementinfo,ringinfo,zusatz=None):
        
        self.ring = None


    # Die Beschreibung soll immer so aussehen:
    # "Ringelement  in Ring"
    # Für die Ausgabe von "Ringelement" ist drucke_element zuständig.
    # Dies muss noch implementiert werden.
    # Die Zusammensetzung ist dann immer gleich.
    # Deshalb ist __str__ nicht abstrakt.
    # (Und __repr__ ist schon in MeinABCObjekt implementiert.)
    # Daneben gibt es noch die Methode drucke_element_mit_klammern.
    # Dies wird von der Ausgabemethode für Polynomringelement
    # aufgerufen.
    # Es werden nur dann Klammern um das Element gesetzt, 
    # wenn dies notwendig ist.
    # In diesem Sinne wird dies erstmal durch drucke_element implementiert.
    
        
    @abstractmethod
    def drucke_element(self):
        pass


    def drucke_element_mit_klammern(self):

        return self.drucke_element()


    def __str__(self):
        
        return self.drucke_element() + "  in " + self.ring.__str__()

    

    
    @abstractmethod   
    def __eq__(self,other):

        if not type(self) == type(other):
            return False

        if not self.ring == other.ring:
            return False

        return True
        
        
    def umgebung(self):
        return self.ring

    # +x ist x:
    def __pos__(self):
        
        return self

    
    @abstractmethod   
    def __neg__(self):
        pass
    
    @abstractmethod   
    def __add__(self,other):
        
        if not type(self) == type(other):
            raise TypeError("Die Elemente sind nicht aus vergleichbaren Ringen.")

        if not self.ring == other.ring:
            raise RuntimeError("Die Ringe stimmen nicht überein.")

        return True

    # a - b ist a + (-b):
    def __sub__(self,other):
        
        return self + (- other)
    

    # Multiplikation mit Ringelement links (d.h. other ist rechts).
    # Wichtig: Die normale Multiplikation __mul__ darf nur für
    # Ringelemente implemtiert sein. Das lässt dann offen, was bei
    # e*x, x kein Ringlement, passiert.
    # "Lögischer" wäre eigentlich: __mul__ wird gar nicht implemtiert
    # und dann ruft python immer __rmul__ auf. Das funktioniert aber
    # nicht, wenn self und other denselben Typ haben.
    
    
    def __mul__(self,other):
        
        if not type(self) == type(other):
            return NotImplemented
    
        return other.__rmul__(self)

    
    @abstractmethod
    def __rmul__(self,other):
        
        if not (type(other) == int or isinstance(other,RingElement)):
            raise TypeError("Das erste Objekt ist keine Zahl und kein Ringelement.")

        return True


    # invers und truediv könnten in einer
    # Implementierung auch "geht nicht"
    # zurückgeben.
    
    @abstractmethod
    def invers(self):
        pass


    # Wenn man invertieren kann, kann man auch
    # dividieren:
    
    def __truediv__(self,other):
    
        if type(self) != type(other):
            raise TypeError()
    
        return self*other.invers()

            
    #Dies ist für a^b, Eingabe: a ** b:
 
    def __pow__(self,exponent):
    
        if not isinstance(exponent,int):
            raise TypeError()
        
        if exponent < 0:
            self = self.invers()
            exponent = -exponent
            
        # Jetzt kommt square-and-multiply
        # Der Exponent wird 2-adisch dargestellt.
        # Die Funktion dafür ist darunter.
        
        a = self
 
        zweiadisch = ZweiAdisch(exponent)

        c = self.ring.eins

        for i in range (0,len(zweiadisch)-1):
            if zweiadisch[i] == '1':
                c = a*c
            c = c*c

        # Am Ende muss man noch einmal addieren, ohne zu multiplizieren.
     
        if len(zweiadisch) > 0 and zweiadisch[len(zweiadisch)-1] == '1':
            c = a*c

        return c


        
    @staticmethod        
    def intmult(n,ele):

        if not isinstance(ele,RingElement):
            return TypeError("Zweites Objekt ist kein Ringelement.")

        if not type(n) == int:
            return TypeError("Das erste Objekt ist keine ganze Zahl...")

        zweiadisch = ZweiAdisch(n)

        c = ele.ring.null

        for i in range (0,len(zweiadisch)-1):
            if zweiadisch[i] == '1':
                c = c + ele
            c = c + c

        # Am Ende muss man noch einmal addieren, ohne zu multiplizieren.
     
        if (len(zweiadisch) > 0 
                and zweiadisch[len(zweiadisch)-1] == '1'):
            c = c + ele

        return c

#----------------------------------------------
# class InvertierungsFehler
# Fehler für das Fehlschlagen der Invertierung

    
class InvertierungsFehler(ArithmeticError):

    def __init__(self,element):

        self.message = element
        super().__init__("{0} ist nicht invertierbar.".format(element.__str__())
)
    

#----------------------------------------------------------
# Funktion ZweiAdisch
    
# Eine natürliche Zahl wird in zwei-adische Darstellung umgewandelt.
# Die Reihenfolge der bits ist "so wie man schreibt",
# d.h. die letzte Stelle gibt an, ob gerade oder ungerade

def ZweiAdisch(a):

    if not isinstance(a,int):
        raise TypeError()
 
    if a < 0:
        raise RuntimeError("Die Zahl ist negativ.")

    s = ""
    while a != 0:
        bit = a % 2
        a = a//2
        s = str(bit) +s
    return s


#----------------------------------------------------
# Instanziierbare Klasse Ganzzahlring
# Da der Typ int schon existiert, gibt es (leider)
# keine Klasse GanzzahlringElement.


class Ganzzahlring(Ring):

    def __init__(self): 
        
        self.null, self.eins = 0,1
    
        self._frier()
        
         
    def __str__(self):
        return "Z"


 

    def element(self,ele):

        if not type(ele) == int:
            raise TypeError("Element ist keine ganze Zahl.")
        return ele

    
    
    @staticmethod
    # Berechnung von ggT(a,b) und u,v mit ua + vb = ggT(a,b):
    # 'geklaut' von http://www.inf.fh-flensburg.de/lang/krypto/algo/euklid.htm
    # Die Methode fuer ElementRestklassenring.invers() ist hiervon adaptiert.

    def ExtGGT(a, b):
        if not (isinstance(a,int) and isinstance(b,int)):
            raise TypeError()
            
        u, v, s, t = 1, 0, 0, 1
        while b!=0:
            q=a//b
            a, b = b, a-q*b
            u, s = s, u-q*s
            v, t = t, v-q*t
        return a, u, v


    

# Und dann initialisieren wir gleich mal Z:
Z = Ganzzahlring()


#------------------------------------------
# Instanziierbare Klasse RingTupel

class RingTupel(MeinABCObjekt):
    
    def __init__(self,eingabe1,eingabe2 = None, ring = None):

        # Es gibt mehrere sinnvolle Eingaben:
        
        # eingabe1 : Liste (list) von Ringelementen, möglicherweise eingabe2 : Ring
        # eingabe1 : Tupel (tuple) von Ringelementen, möglicherweise eingabe2 : Ring
        # Hier kann "Ringelement" entweder eine Instanz von RingElement
        # oder von int sein.

        # eingabe1 : RingTupel, möglicherweise eingabe2 : Ring

        # alles drei soll dann ein Tupel von Elementen in dem Ring ergeben

        # standardmäßig ist der Ring durch das erste Ringelement gegeben
        
        # eingabe1 : Ringelement, eingabe2 : nicht-negative ganze Zahl,
        #    möglicherweise ring : Ring
        # Dies soll ein Tupel der Länge eingabe2 mit einem Eintrag eingabe1
        # als Element von Ring sein.
        # Standardäßig ist der Ring durch das Ringelement gegeben.

        if isinstance(eingabe2,Ring) and ring == None:

            ring = eingabe2
            eingabe2 = None


        # Jetzt erstmal die Ringelemente kopieren:
        eingabe1 = deepcopy(eingabe1)
            
        self.ring = ring
            
        # Jetzt ist nur noch sinnvoll:
        # eingabe1: Liste oder Tupel von Ringelementen oder RingTupel,
        #                          eingabe2 : None,
        # oder:
        # eingabe1: Ringelement, eingabe2 : int

        # Ferner ist nun self.ring entweder None oder eben der angegebene Ring.
        
        if eingabe2 == None:
        # Nur eine Eingabe (bis auf möglicherweise den Ring).
        # Dann sollte diese eine Liste oder ein Tupel oder vom Typ RingTupel sein.
        
            if type(eingabe1) == list:
            # Die eine Eingabe ist eine Liste.
            # Dann wird sie einfach übertragen.
                self.koeffizienten = eingabe1
            
            elif type(eingabe1) == tuple:
            # Die eine Eingabe ist ein Tupel.
            # Dann wird es in eine Liste verwandelt und übertragen.
            
                self.koeffizienten = []
                for i in range(0,len(eingabe1)):
                    self.koeffizienten += [eingabe1[i]]


            elif type(eingabe1) == RingTupel:
                self.koeffizienten = eingabe1.koeffizienten
                    
            else:
                raise TypeError("Es wurde keine Länge angegeben. Deshalb wurde das erste Objekt als eine Liste oder ein Tupel von Ringelementen (RingElement oder int) oder vom Typ RingTupel erwartet. Dies war nicht der Fall.")


        elif type(eingabe2) == int:
        # Jetzt wird eine Liste der Länge eingabe2 vom Element eingabe1 erzeugt

            if eingabe2 < 0:
                RuntimeError("Die angegebene Länge ist negativ.")

            self.koeffizienten = []
            for i in range(0,eingabe2):
                self.koeffizienten += [eingabe1]

                
        else:
            raise RuntimeError("Zu diesen Daten kann kein Objekt vom Typ RingTupel erzeugt werden.")            
            

        # Jetzt gibt es self.koeffizienten
            
        self.laenge = len(self.koeffizienten)

        # Wenn die Länge gleich Null ist, ist Schluss.
        if self.laenge == 0:
            if self.ring == None:
                self.ring = Z

        else:
        # Jetzt ist koeffizienten ein nicht-leeres Tupel.
            
        # Die Einträge sollten entweder vom Typ int
        # oder von einem Typ abgeleitet von RingElement sein.
            for i in range(0,len(self.koeffizienten)):
                if not (isinstance(self.koeffizienten[i],RingElement) or type(self.koeffizienten[i]) == int):
                    raise TypeError("Nicht alle Koeffizienten sind Ringelemente.")


            # Wenn nun self.ring noch nicht vorhanden ist, wird es über
            # den ersten Koeffizienten definiert.

            if self.ring == None:

                if isinstance(self.koeffizienten[0],RingElement):
                    self.ring = self.koeffizienten[0].ring
                else: # D.h. koeffizienten[0] ist eine ganze Zahl
                    self.ring = Z
                        
            # Jetzt können die Koeffizienten in diesen Ring abgebildet werden.
            # Ausnahme: der Ring ist Z,
            # dann sollte nur überprüft werden, ob die Koeffizienten
            # ganze Zahlen sind.
            
            if self.ring == Z:
                for i in range(0,self.laenge):
                    if not type(self.koeffizienten[i]) == int:
                        raise TypeError("Der angegebene Ring ist Z, aber nicht alle Koeffizienten sind ganze Zahlen.")

            else:
                for i in range(0,self.laenge):
                    self.koeffizienten[i] = self.ring.element(self.koeffizienten[i])


                                        
    def __str__(self):
        
        rueck = str(self.laenge) + "-er Tupel von Elementen aus dem Ring {0}: \n\n(".format(self.ring) 
        for i in range(0,self.laenge):

            if self.ring == Z:
                rueck = rueck + str(self.koeffizienten[i])

            else:
                rueck = rueck + self.koeffizienten[i].drucke_element()

            if not i == self.laenge-1:
                rueck = rueck + ","
        
        rueck = rueck + ")"

        return rueck
                
    
    def __eq__(self,other):
        
        if not type(self) == type(other):
            return False
        
        return self.koeffizienten == other.koeffizienten
    
         
    def __pos__(self):

            return self
        
    def __neg__(self):
        
        rueck = RingTupel(self.ring.null,self.laenge)
        # Das ist das Nulltupel
            
        for i in range(0,self.laenge):
            rueck.koeffizienten[i] = -self.koeffizienten[i]
        
        return rueck

            
    def __add__(self,other):
        
        if not isinstance(other,RingTupel):
            raise TypeError()
        
        if not self.laenge == other.laenge:
            raise RuntimeError("Die Längen sind nicht gleich.")
        
        if not self.ring == other.ring:
            raise TypeError("Die Elemente sind nicht kompatibel.")
        
        rueck = RingTupel(self.ring.null,self.laenge)
        
        for i in range(0,self.laenge):
            rueck.koeffizienten[i] = self.koeffizienten[i] + other.koeffizienten[i]
        
        return rueck

    
    def __sub__(self,other):
 
        if not isinstance(other,RingTupel):
            raise TypeError()
 
        return self + (-other)
 
    
    def __rmul__(self,other):

        #Wie immer wird hier other*self betrachtet.
                
        # Wir wollen von links mit ganzen Zahlen
        # und mit Ringelementen multiplizieren können.
        # Wenn das Tupel ganze Zahlen enthält, wollen wir ein
        # Tupel von Ringelementen erhalten.
        
        if type(other) == int:
            # Das andere Element ist eine Zahl. 
            # Dann richtet sich der Ring nach self.ring.

            ring = self.ring

            rueck = RingTupel(ring.null,self.laenge)

            for i in range(0,self.laenge):
                rueck.koeffizienten[i] = other*self.koeffizienten[i]
                

            
        elif isinstance(other,RingElement):
            # other ist keine Zahl, aber ein Ringelement.
            # Dann sollte erstmal self ein Tupel von Zahlen
            # oder ein Tupel von Elementen eines vergleichbaren Ringes sein.

            # Der Ring richtet sich nach other, sonst klappt's nicht,
            # wenn self ein Tupel von Zahlen ist.
            
            if self.ring == Z or self.ring == other.ring:
                ring = other.ring

                rueck = RingTupel(ring.null,self.laenge)

                for i in range(0,self.laenge):
                    # In der folgenden Multiplikation muss other
                    # hinten stehen, sonst klappt's nicht, wenn
                    # self ein Tupel von Zahlen ist.
                    rueck.koeffizienten[i] = self.koeffizienten[i]*other
                                        
            else:
                raise RuntimeError("Die Ringe stimmen nicht überein.")

        
        else:
            # Das andere Element ist weder eine Zahl noch ein Ringelement.
            raise TypeError()
 
        return rueck


    def auslaufende_nullen_loeschen(self):

        while self.laenge > 0 and self.koeffizienten[-1] == self.ring.null:
            del self.koeffizienten[-1]
            self.laenge -= 1
       
        
    @staticmethod
    def zusammenfuegen(ringtupel1,ringtupel2):

        if not (isinstance(ringtupel1,RingTupel) and isinstance(ringtupel2,RingTupel)):
            raise TypeError() 

        if ringtupel1 == RingTupel([]):
            return ringtupel2
        
        if ringtupel2 == RingTupel([]):
            return ringtupel1
        
        if not ringtupel1.ring == ringtupel2.ring:
            raise TypeError()

        return RingTupel(ringtupel1.koeffizienten+ringtupel2.koeffizienten)



    
