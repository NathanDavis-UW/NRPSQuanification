import os

from Bio.Blast import NCBIWWW

xml_dir = "BLASTXML"
def blast_execute(record):
    result_handle = NCBIWWW.qblast("blastn", "nt", record.seq)
    save_file = open(os.path.join(xml_dir, "BLAST-" + record.name + ".xml"), "w")
    save_file.write(result_handle.read())
    save_file.close()
    result_handle.close()