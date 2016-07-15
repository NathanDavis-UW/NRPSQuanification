import os
_line_length = 80
stan_dir = "BLASTStandard"
fas_dir = "BLASTFASTA"

def create_dir(d):
    if not os.path.exists(d):
        os.makedirs(d)


def write_blast_standard(i, alignment, hsp, rec_dir):
    create_dir(os.path.join(stan_dir, rec_dir))
    f = open(os.path.join(stan_dir, os.path.join(rec_dir, os.path.join(alignment.title[:alignment.title.index(" ")], alignment.title[:alignment.title.index(" ")] + "-" + str(i) + "-hsp"))), 'w')
    f.write("sequence: " + str(alignment.title) + '\n')
    f.write("length: " + str(hsp.sbjct_end-hsp.sbjct_start) + '\n')
    f.write("e: " + str(hsp.expect) + '\n')
    f.write(str(hsp.query) + '\n')
    f.write(str(hsp.match) + '\n')
    f.write(str(hsp.sbjct) + '\n')


def write_blast_fasta(i, alignment, hsp, rec_dir):
    create_dir(os.path.join(fas_dir, rec_dir))
    f = open(os.path.join(fas_dir, os.path.join(rec_dir, os.path.join(alignment.title[:alignment.title.index(" ")], alignment.title[:alignment.title.index(" ")] + "-" + str(i) + "-hsp"))), 'w')
    if alignment.title[len(alignment.title) - 13:len(alignment.title)] == "complete cds":
        f.write('<' + str(alignment.title[:len(alignment.title) - 12]) + "partial cds" + '\n')
    elif alignment.title[len(alignment.title) - 18:len(alignment.title)] == "complete sequence":
        f.write('<' + str(alignment.title[:len(alignment.title) - 17]) + "partial sequence" + '\n')
    elif alignment.title[len(alignment.title) - 16:len(alignment.title)] == "complete genome":
        f.write('<' + str(alignment.title[:len(alignment.title) - 15]) + "partial genome" + '\n')
    elif alignment.title[len(alignment.title) - 14:len(alignment.title)] == "complete mRNA":
        f.write('<' + str(alignment.title[:len(alignment.title) - 13]) + "partial mRNA" + '\n')
    else:
        f.write('<' + str(alignment.title) + '\n')
    k = 0
    while len(hsp.sbjct[k:len(hsp.sbjct)]) >= _line_length:
        f.write(hsp.sbjct[k:k+_line_length] + '\n')
        k += _line_length
    f.write(hsp.sbjct[k:len(hsp.sbjct)])


def write_full_standard(k, alignment, record):
    f = open(os.path.join(stan_dir, os.path.join(record.name, record.name + "-" + str(k) + "-alignment-" + alignment.title[:alignment.title.index(" ")])), 'w')
    f.write("sequence: " + str(alignment.title) + '\n')
    f.write("length: " + str(alignment.length) + '\n')
    f.write("description: " + str(alignment.hit_def) + '\n')
    #ar = []
    #for hsp in alignment.hsps:
    #    a = 0
    #    while len(record.seq) - len(hsp.sbjct) >= a:
    #        if record.seq[a:a+len(hsp.sbjct)] == hsp.sbjct:
    #            for i in range(len(hsp.sbjct)):
    #                ar.insert(a+i, hsp.sbjct[i])
    #            break
    #        else:
    #            a += 1
    #f.write(str(record.seq) + '\n')
    #for value in ar:
    #    if value is not None:
    #        f.write("|")
    #f.write('\n')
    #for value in ar:
    #    if value is not None:
    #        f.write(value)
