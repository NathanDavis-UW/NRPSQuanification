import os

import DecTreeGenerator
import csvGenerator
import SeqGrabber

csv_dir = "NRPSCSV"
hsp_target = "sequence"
non_target = "non-specific sequence"
tree_dir = "Tree"
csvGenerator.simple_dir(tree_dir)
nrps_dir = "NRPS"
csvGenerator.simple_dir(nrps_dir)
ana_dir = "Analysis"
dot_dir = "TreeDot"
png_dir = "TreePng"
key_dir = "TreeKey"
hsp_dir = "HSP-specific"
non_dir = "non-specific"
seq_dir = "NRPSSequences"

def construct_tree():
    #csvGenerator.create_csv()
    csvGenerator.create_dir(seq_dir, nrps_dir)
    if os.path.exists(os.path.join(ana_dir, os.path.join(nrps_dir, csv_dir))):
        csvGenerator.create_dir(dot_dir, tree_dir)
        csvGenerator.create_dir(png_dir, tree_dir)
        csvGenerator.create_dir(key_dir, tree_dir)
        csv_files = []
        for [dirpath, dirname, filename] in os.walk(os.path.join(ana_dir, os.path.join(nrps_dir, csv_dir))):
            csv_files.extend(filename)
        for file in csv_files:
            csvGenerator.create_dir(os.path.join(png_dir, file[:len(file) - 4]), tree_dir)
            csvGenerator.create_dir(os.path.join(seq_dir, file[:len(file) - 4]), nrps_dir)
            csv = DecTreeGenerator.get_blast_data(file)

            for sequence in csv[non_target].unique():
                alt_sequence = ""
                alt_sequence += sequence[:sequence.index("|")+1]
                sequence = sequence[sequence.index("|")+1:]
                alt_sequence += sequence[:sequence.index("|")]
                SeqGrabber.get_seq(alt_sequence, file[:len(file) -  4])
            #create_tree(hsp_dir, DecTreeGenerator.encode_blast(csv, hsp_target), file)
            #create_tree(non_dir, DecTreeGenerator.encode_blast(csv, non_target), file)

def create_tree(dir, alt_csv, file):
    csvGenerator.create_dir(os.path.join(png_dir, os.path.join(file[:len(file) - 4], dir)), tree_dir)
    csvGenerator.create_dir(os.path.join(key_dir, dir), tree_dir)
    csvGenerator.create_dir(os.path.join(dot_dir, os.path.join(file[:len(file) -4], dir)), tree_dir)
    DecTreeGenerator.build_tree(alt_csv, file, [alt_csv.columns[4]], dir)
    DecTreeGenerator.build_tree(alt_csv, file, [alt_csv.columns[4], alt_csv.columns[5]], dir)
    DecTreeGenerator.build_tree(alt_csv, file, [alt_csv.columns[4], alt_csv.columns[5], alt_csv.columns[2]], dir)
    DecTreeGenerator.create_key(alt_csv, file, dir)