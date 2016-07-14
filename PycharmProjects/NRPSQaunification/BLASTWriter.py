import os
_line_length = 80


def create_dir(d):
    if not os.path.exists(d):
        os.makedirs(d)


def write_blast_standard(i, alignment, hsp, record):
    stan_dir = "BLASTStandard"
    sub_dir = record.name
    create_dir(os.path.join(stan_dir, sub_dir))
    f = open(os.path.join(stan_dir, os.path.join(sub_dir, stan_dir + str(i) + "-" + record.name)), 'w')
    f.write("sequence: " + str(alignment.title) + '\n')
    f.write("length: " + str(alignment.length) + '\n')
    f.write("e: " + str(hsp.expect) + '\n')
    f.write("description: " + str(alignment.hit_def) + '\n')
    f.write(str(hsp.query) + '\n')
    f.write(str(hsp.match) + '\n')
    f.write(str(hsp.sbjct) + '\n')


def write_blast_fasta(i, alignment, hsp, record):
    fas_dir = "BLASTFASTA"
    sub_dir = record.name
    create_dir(os.path.join(fas_dir, sub_dir))
    f = open(os.path.join(fas_dir, os.path.join(sub_dir, fas_dir + str(i) + "-" + record.name)), 'w')
    f.write('<' + str(alignment.title) + '\n')
    k = 0
    while len(hsp.sbjct[k:len(hsp.sbjct)]) >= _line_length:
        f.write(hsp.sbjct[k:k+_line_length] + '\n')
        k += _line_length
    f.write(hsp.sbjct[k:len(hsp.sbjct)])

