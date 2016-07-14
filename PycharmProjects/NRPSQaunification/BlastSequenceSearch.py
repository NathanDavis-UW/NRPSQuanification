import os

from Bio import SeqIO
from Bio.Blast import NCBIXML

import BLASTWriter

root_dir = "RootNRPSs"
BLASTWriter.create_dir(root_dir)
xml_dir = "BLASTXML"
BLASTWriter.create_dir(xml_dir)
stan_dir = "BLASTStandard"
BLASTWriter.create_dir(stan_dir)
fas_dir = "BLASTFASTA"
main_dir = []
for [dirpath, dirname, filename] in os.walk(root_dir):
    main_dir.extend(filename)
for file in main_dir:
    if file[0:len(file)-4] not in os.listdir(stan_dir):
        record = SeqIO.read(os.path.join(root_dir, file), format="gb")
        #BLASTExecute.blast_execute(record)
        result_handle = open(os.path.join(xml_dir, "BLAST-" + record.name + ".xml"))
        blast_record = NCBIXML.read(result_handle)
        i = 0
        e_threshold = .001
        for alignment in blast_record.alignments:
            for hsp in alignment.hsps:
                if hsp.expect < e_threshold:
                    i += 1
                    BLASTWriter.write_blast_standard(i, alignment, hsp, record)
                    BLASTWriter.write_blast_fasta(i, alignment, hsp, record)
