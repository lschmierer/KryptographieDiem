from abc import abstractmethod

from tocas.AbstrakterAnfang import UnveraenderbaresObjekt


class AdditiveGruppe(UnveraenderbaresObjekt):
    """Abstrakte Klasse für additive Gruppen, angelehnt an Klasse Ring."""

    def __eq__(self, other):
        if not type(self) == type(other):
            return False

        return True

    @abstractmethod
    def element(self, *info):
        """Neues Element aus der Gruppe."""
        pass

    @abstractmethod
    def ist_endlich(self, *info):
        """Ist Gruppe endlich."""
        pass


class AdditiveGruppenElement(UnveraenderbaresObjekt):
    """Abstrakte Klasse für Elemente aus additiber Gruppen, angelehnt an Klasse RingElement."""

    @abstractmethod
    def __init__(self):
        self.gruppe = None

    @abstractmethod
    def drucke_element(self):
        pass

    def drucke_element_mit_klammern(self):
        return self.drucke_element()

    def __str__(self):
        return self.drucke_element() + "  in " + self.gruppe.__str__()

    @abstractmethod
    def __eq__(self, other):
        if not type(self) == type(other):
            return False
        if not self.gruppe == other.gruppe:
            return False
        return True

    def umgebung(self):
        return self.gruppe

    def __pos__(self):
        return self

    @abstractmethod
    def __neg__(self):
        pass

    @abstractmethod
    def __add__(self, other):
        if not type(self) == type(other):
            raise TypeError(
                "Die Elemente sind nicht aus vergleichbaren Gruppen.")

        if not self.gruppe == other.gruppe:
            raise RuntimeError("Die Gruppen stimmen nicht überein.")

        return True

    def __sub__(self, other):
        return self + (- other)

    @abstractmethod
    def __mul__(self, other):
        if type(other) != int:
            raise TypeError('Multiplikation nur mit Skalaren möglich.')

    def __rmul__(self, other):
        return self.__mul__(other)

    @abstractmethod
    def zwei_adisch(self):
        """Gibt eine zwei adische Darstellung zurück.

        Der Rückgabewert ist ein Tupel der aus der zwei adischen Darstellung
        (als int) und der maximalen Anzahl an Bits, die ein Element in der Umgebung
        in zwei adischer Form besitzen kann, besteht.
        """
        pass

    @abstractmethod
    def __hash__(self):
        pass
