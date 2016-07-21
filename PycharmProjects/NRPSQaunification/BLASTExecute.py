import os

from Bio.Blast import NCBIWWW
ana_dir = "Analysis"
bla_dir = "BLAST"
xml_dir = "BLASTXML"
def blast_execute(record):
    result_handle = NCBIWWW.qblast("blastn", "nt", record.seq)
    save_file = open(os.path.join(ana_dir, os.path.join(bla_dir,
                    os.path.join(xml_dir, "BLAST-" + record.name + ".xml"))), "w")
    save_file.write(result_handle.read())
    save_file.close()
    result_handle.close()