import os

from Bio import SeqIO

fas_dir = "BLASTFASTARaw"
records = []
results = []
rec_num = 0
for file in fas_dir:
    records.append(SeqIO.read(os.path.join(fas_dir, file), format="fasta"))
for rec in records:
    for comp_rec in records:
        if not rec.name == comp_rec.name:
            for i in range(len(rec.seq)):
                if i > len(comp_rec.seq):
                    results[rec_num] += 0
                elif rec.seq(i) == comp_rec.seq(i):
                    results[rec_num] += 1
                else:
                    results[rec_num] -= 1
    rec_num += 1