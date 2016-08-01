import os
_line_length = 80
stan_dir = "BLASTStandard"
fas_dir = "BLASTFASTA"
Fraw_dir = "BLASTFASTARaw"
Sraw_dir = "BLASTStandardRaw"
ana_dir = "Analysis"
bla_dir = "BLAST"


# creates a directory that does not sit inside a non-major sub-directory
def simple_dir(d):
    if not os.path.exists(os.path.join(ana_dir, d)):
        os.makedirs(os.path.join(ana_dir, d))


# creates a directory that does sit inside a non-major sub-directory
def create_dir(f, dir):
    if not os.path.exists(os.path.join(ana_dir, os.path.join(dir, f))):
        os.makedirs(os.path.join(ana_dir, os.path.join(dir, f)))


# takes an array of strings and turns it into a text file
def create_blast_files(f, str_arr):
    for s in str_arr:
        f.write(s)


# creates an array of strings that contain info for a standard blast info file
def write_blast_standard(i, alignment, hsp, rec_dir):
    f = []
    f.append("sequence: " + str(alignment.title[:alignment.title.index(" ")] + "-" + str(i)) + '\n')
    f.append("length: " + str(abs(hsp.sbjct_end-hsp.sbjct_start)) + '\n')
    write_sequence('description: ', f, alignment)
    f.append("e: " + str(hsp.expect) + '\n')
    f.append("weighted e: " + str(hsp.expect * (pow(10, 37))) + '\n')
    f.append("score: " + str(hsp.score) + '\n')
    f.append("adjusted score: " + str(hsp.score/abs(hsp.sbjct_end-hsp.sbjct_start)) + '\n')
    f.append(str(hsp.query) + '\n')
    f.append(str(hsp.match) + '\n')
    f.append(str(hsp.sbjct) + '\n')
    return f


# creates an array of strings that contain info for a fasta blast info file
def write_blast_fasta(i, alignment, hsp, rec_dir):
    f = []
    write_sequence('<', f, alignment)
    k = 0
    while len(hsp.sbjct[k:len(hsp.sbjct)]) >= _line_length:
        f.append(hsp.sbjct[k:k+_line_length] + '\n')
        k += _line_length
    f.append(hsp.sbjct[k:len(hsp.sbjct)])
    return f


# writes a full summary of an alignment rather than being hsp specific like other blast standard  info files.
def write_full_standard(k, alignment, record):
    f = open(os.path.join(ana_dir, os.path.join(bla_dir, os.path.join(stan_dir, os.path.join(record.name, record.name + "-" + str(k) + "-alignment-" + alignment.title[:alignment.title.index(" ")])))), 'w')
    f.write("sequence: " + str(alignment.title[:alignment.title.index(" ")]) + '\n')
    f.write("length: " + str(abs(alignment.length)) + '\n')
    f.write("description: " + str(alignment.hit_def) + '\n')


# writes that header for either a standard or fasta blast info file and replaces complete descriptor with partial to
# illustrate tha these files display hsps
def write_sequence(header, main, alignment):
    if alignment.hit_def[len(alignment.hit_def) - 12:len(alignment.hit_def)] == "complete cds":
        main.append(header + str(alignment.hit_def[:len(alignment.hit_def) - 12]) + "partial cds" + '\n')
    elif alignment.hit_def[len(alignment.hit_def) - 17:len(alignment.hit_def)] == "complete sequence":
        main.append(header + str(alignment.hit_def[:len(alignment.hit_def) - 17]) + "partial sequence" + '\n')
    elif alignment.hit_def[len(alignment.hit_def) - 15:len(alignment.hit_def)] == "complete genome":
        main.append(header + str(alignment.hit_def[:len(alignment.hit_def) - 15]) + "partial genome" + '\n')
    elif alignment.hit_def[len(alignment.hit_def) - 13:len(alignment.hit_def)] == "complete mRNA":
        main.append(header + str(alignment.hit_def[:len(alignment.hit_def) - 13]) + "partial mRNA" + '\n')
    else:
        main.append(header + str(alignment.hit_def) + '\n')