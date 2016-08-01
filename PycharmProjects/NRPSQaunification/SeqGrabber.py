import os

from Bio import Entrez

search_database = 'nucleotide'
Entrez.email = 'n.j.davis.college@gmail.com'
nrps_dir = "NRPS"
seq_dir = "NRPSSequences"
ana_dir = "Analysis"


# searches for a sequence based on ID and returns its info
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


# processes the sequences name to see if it is a match
def process_seq(seqs, comp_rec):
    results = []
    rec_num = 0
    for rec in seqs:
        if not rec.name == comp_rec.name:
            Cseq = ""
            for i in range(len(rec.seq)):
                Cseq += rec.seq(i)
                if i > len(comp_rec.seq):
                    results[rec_num] += 0
                elif rec.seq(i) == comp_rec.seq(i):
                    results[rec_num] += 2
                else:
                    results[rec_num] -= 1
        rec_num += 1