import abc


class AminoAcid:
    @abc.abstractmethod
    def __iter__(self):
        pass

    @abc.abstractmethod
    def getApr(self):
        pass

    @abc.abstractmethod
    def getBpr(self):
        pass

    @abc.abstractmethod
    def getBint(self):
        pass

    @abc.abstractmethod
    def getAint(self):
        pass


class I(AminoAcid):
    def __iter__(self):
        pass

    def getApr(self):
        return .41

    def getBpr(self):
        return .1

    def getAint(self):
        return 0

    def getBint(self):
        return 1


class V(AminoAcid):
    def __iter__(self):
        pass

    def getApr(self):
        return .61

    def getBpr(self):
        return .13

    def getAint(self):
        return -1

    def getBint(self):
        return 1


class T(AminoAcid):
    def __iter__(self):
        pass

    def getApr(self):
        return .66

    def getBpr(self):
        return .06

    def getAint(self):
        return -1

    def getBint(self):
        return 1


class F(AminoAcid):
    def __iter__(self):
        pass

    def getApr(self):
        return .54

    def getBpr(self):
        return .13

    def getAint(self):
        return 0

    def getBint(self):
        return 1


class Y(AminoAcid):
    def __iter__(self):
        pass

    def getApr(self):
        return .53

    def getBpr(self):
        return .11

    def getAint(self):
        return 0

    def getBint(self):
        return 1


class E(AminoAcid):
    def __iter__(self):
        pass

    def getApr(self):
        return .4

    def getBpr(self):
        return .35

    def getAint(self):
        return 0

    def getBint(self):
        return 0


class Q(AminoAcid):
    def __iter__(self):
        pass

    def getApr(self):
        return .39

    def getBpr(self):
        return .34

    def getAint(self):
        return 0

    def getBint(self):
        return 0


class C(AminoAcid):
    def __iter__(self):
        pass

    def getApr(self):
        return .68

    def getBpr(self):
        return .25

    def getAint(self):
        return -1

    def getBint(self):
        return 1


class L(AminoAcid):
    def __iter__(self):
        pass

    def getApr(self):
        return .21

    def getBpr(self):
        return .32

    def getAint(self):
        return 1

    def getBint(self):
        return 0


class K(AminoAcid):
    def __iter__(self):
        pass

    def getApr(self):
        return .26

    def getBpr(self):
        return .34

    def getAint(self):
        return 1

    def getBint(self):
        return 0


class S(AminoAcid):
    def __iter__(self):
        pass

    def getApr(self):
        return .5

    def getBpr(self):
        return .3

    def getAint(self):
        return 0

    def getBint(self):
        return 0


class R(AminoAcid):
    def __iter__(self):
        pass

    def getApr(self):
        return .21

    def getBpr(self):
        return .35

    def getAint(self):
        return 1

    def getBint(self):
        return -1


class M(AminoAcid):
    def __iter__(self):
        pass

    def getApr(self):
        return .24

    def getBpr(self):
        return .26

    def getAint(self):
        return 1

    def getBint(self):
        return 0


class H(AminoAcid):
    def __iter__(self):
        pass

    def getApr(self):
        return .61

    def getBpr(self):
        return .37

    def getAint(self):
        return -1

    def getBint(self):
        return -1


class W(AminoAcid):
    def __iter__(self):
        pass

    def getApr(self):
        return .49

    def getBpr(self):
        return .24

    def getAint(self):
        return 0

    def getBint(self):
        return 1


class A(AminoAcid):
    def __iter__(self):
        pass

    def getApr(self):
        return 0

    def getBpr(self):
        return .47

    def getAint(self):
        return 1

    def getBint(self):
        return -1


class D(AminoAcid):
    def __iter__(self):
        pass

    def getApr(self):
        return .69

    def getBpr(self):
        return .72

    def getAint(self):
        return -1

    def getBint(self):
        return -1


class N(AminoAcid):
    def __iter__(self):
        pass

    def getApr(self):
        return .65

    def getBpr(self):
        return .4

    def getAint(self):
        return -1

    def getBint(self):
        return -1


class G(AminoAcid):
    def __iter__(self):
        pass

    def getApr(self):
        return 1

    def getBpr(self):
        return .3

    def getAint(self):
        return -1

    def getBint(self):
        return 0


class P(AminoAcid):
    def __iter__(self):
        pass

    def getApr(self):
        return 1

    def getBpr(self):
        return .3

    def getAint(self):
        return -1

    def getBint(self):
        return 0

