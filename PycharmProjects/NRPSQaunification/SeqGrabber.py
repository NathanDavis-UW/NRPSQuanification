import os

from Bio import Entrez

search_database = 'nucleotide'
Entrez.email = 'n.j.davis.college@gmail.com'
nrps_dir = "NRPS"
seq_dir = "NRPSSequences"
ana_dir = "Analysis"


def get_seq(alignment, root_dir):
    search_term = alignment
    handle = Entrez.esearch(db=search_database, term=search_term)
    record = Entrez.read(handle)
    for i_d in record["IdList"]:
        filename = os.path.join(ana_dir, os.path.join(nrps_dir, os.path.join(seq_dir,
                       os.path.join(root_dir, "NRPSGeneralInfo_" + i_d + ".gbk"))))
        if not os.path.isfile(filename):
            new_handle = Entrez.efetch(db=search_database, id=i_d, rettype="gb", retmode="text")
            out_handle = open(filename, "w")
            out_handle.write(new_handle.read())
            out_handle.close()
            new_handle.close()

def process_seq(seqs):
