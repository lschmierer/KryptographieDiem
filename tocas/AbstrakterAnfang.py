from abc import ABC, abstractmethod


#-----------------------------------------
# Funktion Typbeschreibung

# Dies gibt zu einer Instanz einer Klasse den Namen der Klasse als String zurück.
# Anders ausgedrückt: Es gibt den Namen (!) des Typs zurück
# Denn: type(objekt) ist identisch zu objekt.__class__

def TypBeschreibung(objekt):

    return objekt.__class__.__name__


#----------------------------------------
# Abstrakte Klasse MeinABCObjekt(ABC)


# Der Grund für diese rudimentäre abstrakte Klasse ist dieser:

# __str__ wird mit print(.) ausgeben.
# __repr__ wird ausgegeben, wenn man einfach
# den Objektnamen eingibt.
# Nun wird von __repr__ auf __str__ verwiesen.


class MeinABCObjekt(ABC):

    @abstractmethod
    def __init__(self):
        pass

          
    @abstractmethod
    def __str__(self):
        pass
    
    # Hier wird also immer dasselbe ausgegeben.
       
    def __repr__(self):
   
        return self.__str__()
   


#-------------------------------------------------------
# Abstrakte Klasse UnveraenderbaresObjekt(MeinABCObjekt)


# Die folgende Idee zum "Einfrieren" von Klassen habe ich hier "geklaut"
# https://stackoverflow.com/questions/3603502/prevent-creating-new-attributes-outside-init

# Zum Einfrieren benutzt man dann das Kommando self._frier().


class UnveraenderbaresObjekt(MeinABCObjekt):

    @abstractmethod
    def __init__(self):
        pass
       
    _unveraenderbar = False

    def __setattr__(self, key, value):
        if self._unveraenderbar:
            raise TypeError( "{0}-Objekt ist unveränderbar.".format(TypBeschreibung(self)))
        object.__setattr__(self, key, value)

    def _frier(self):
        self._unveraenderbar = True
        
