import os

from Bio import SeqIO

fas_dir = "BLASTFASTA"
records = []
for file in fas_dir:
    records.append(SeqIO.read(os.path.join(fas_dir, file), format="fasta"))