import sys

from Sequence import Sequence

s = input('input amino acid sequence')
sys.stdout.write(s + '\n')
sq = Sequence(s)
k = 0
a = sq.AStartLoc(sq.getseq())
b = sq.BStartLoc(sq.getseq())
for i in range(len(s) - 1):
    if len(a) > 0:
        if a[k][0] <= i <= a[k][1]:
            sys.stdout.write('A')
        else:
            sys.stdout.write(' ')
        if a[k][1] == i and k < len(a) - 1 :
            k += 1
print('\n')
k = 0
for i in range(len(s) - 1):
    if len(b) > 0:
        if b[k][0] <= i <= b[k][1]:
            sys.stdout.write('B')
        else:
            sys.stdout.write(' ')
        if b[k][1] == i and len(b) < k:
            k += 1