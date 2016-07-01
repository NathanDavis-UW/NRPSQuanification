from AminoAcid import *


class Sequence:
    def __init__(self, sequence):
        self.sequence = self.initiate(sequence)
        self.a = []
        self.b = []

    def getseq(self):
        return self.sequence

    def initiate(self, sequence):
        seq = []
        for char in sequence:
            if char == 'M':
                seq.append(M())
            elif char == 'I':
                seq.append(I())
            elif char == 'V':
                seq.append(V())
            elif char == 'T':
                seq.append(T())
            elif char == 'F':
                seq.append(F())
            elif char == 'Y':
                seq.append(Y())
            elif char == 'E':
                seq.append(E())
            elif char == 'Q':
                seq.append(Q())
            elif char == 'C':
                seq.append(C())
            elif char == 'L':
                seq.append(L())
            elif char == 'K':
                seq.append(K())
            elif char == 'S':
                seq.append(S())
            elif char == 'R':
                seq.append(R())
            elif char == 'H':
                seq.append(H())
            elif char == 'W':
                seq.append(W())
            elif char == 'A':
                seq.append(A())
            elif char == 'D':
                seq.append(D())
            elif char == 'N':
                seq.append(N())
            elif char == 'G':
                seq.append(G())
            elif char == 'P':
                seq.append(P())
        return seq


    def AStartLoc(self, seq):
        i = 0
        while i < len(seq) - 6:
            st = []
            for k in range(6):
                st.append(seq[i + k])
            count = 0

            while k > 0 and st[k].getAint() != -1:
                if st[k].getAint() == 1:
                    count += 1
                k -= 1
            if st[k].getAint() == 1:
                count += 1
            if count > 3 and k == 0:
                full = len(self.Aextend(st, seq, i))
                self.a.append([i, i + full])
                i += full;
            else:
                i += 1
        return self.a

    def Aextend(self, st, seq, i):
        av = 0.0;
        avnum = 0
        avfin = 0
        for int in range(len(st) - 1):
            avnum += 1
            av = (av + st[int].getApr())
            avfin = av / avnum
        int += 1
        avnum += 1
        av = (av + seq[i + int].getApr())
        avfin = av / avnum
        while avfin < .3 and not seq[i + int].getAint() == -1 and i + int < len(seq) - 1:
            st.append(seq[i + int])
            int += 1
            avnum += 1
            av = (av + seq[i + int].getApr())
            avfin = av / avnum
        return st


    def BStartLoc(self, seq):
        i = 0
        while i < len(seq) - 6:
            st = []
            for k in range(6):
                st.append(seq[i + k])
            count = 0
            while k > 0 and st[k].getBint() != -1:
                k -= 1
                if st[k].getBint() == 1:
                    count += 1
            if count > 4 and k == 0:
                full = len(self.Bextend(st, seq, i))
                self.b.append([i, i + full])
                i += full;
            else:
                i = i + 5 - k
        return self.b

    def Bextend(self, st, seq, i):
        av = 0.0;
        avnum = 0
        avfin = 0
        for int in range(len(st) - 1):
            avnum += 1
            av = (av + st[int].getBpr())
            avfin = av / avnum
        int += 1
        avnum += 1
        av = (av + seq[i + int].getBpr())
        avfin = av / avnum
        while avfin < .25 and not seq[i + int].getBint() == -1 and i + int < len(seq) - 1:
            st.append(seq[i + int])
            int += 1
            avnum += 1
            av = (av + seq[i + int].getBpr())
            avfin = av / avnum
        return st
