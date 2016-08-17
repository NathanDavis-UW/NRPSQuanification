import os

import DecTreeGenerator
import csvGenerator
import SeqGrabber

# statement of constants
csv_dir = "NRPSCSV"
hsp_target = "sequence"
non_target = "non-specific sequence"
classifier = "NRPS Classifier"
dual_classifier = "NRPS-PKS Classifier"
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


# generates csv files with csv generator and then uses them to create dataframes and graphical representations of those
# dataframes
def construct_tree(tree_analysis, tree_type, hsp_files):
    csvGenerator.create_dir(seq_dir, nrps_dir)
    if os.path.exists(os.path.join(ana_dir, os.path.join(nrps_dir, csv_dir))):
        csvGenerator.create_dir(dot_dir, tree_dir)
        csvGenerator.create_dir(png_dir, tree_dir)
        csvGenerator.create_dir(key_dir, tree_dir)
        csv_files = []
        for arr in os.walk(os.path.join(ana_dir, os.path.join(nrps_dir, csv_dir))):
            csv_files.extend(arr[2])
        i = 0
        for file in csv_files:
            if file[0:len(file) - 4] not in os.listdir(os.path.join(ana_dir, os.path.join(nrps_dir, csv_dir))) and file[
                   0:len(file) - 4] in tree_analysis:
                csvGenerator.create_dir(os.path.join(png_dir, file[:len(file) - 4]), tree_dir)
                csvGenerator.create_dir(os.path.join(seq_dir, file[:len(file) - 4]), nrps_dir)
                csv = DecTreeGenerator.get_blast_data(file)

                # this cuts down the name of the sequence to a more readable format for the tree
                for sequence in csv[non_target].unique():
                    alt_sequence = ""
                    alt_sequence += sequence[:sequence.index("|")+1]
                    sequence = sequence[sequence.index("|")+1:]
                    alt_sequence += sequence[:sequence.index("|")]
                    if not os.path.exists(os.path.join(ana_dir, os.path.join(nrps_dir, seq_dir))):
                        SeqGrabber.get_seq(alt_sequence, file[:len(file) - 4])

                # This checks whether the user wanted specific sequence non-specific sequences or both, then creates
                # the trees proper
                if hsp_files[0].get() == 1:
                    csv = SeqGrabber.filter_csv(csv, file[0: len(file) - 4])
                    create_tree(hsp_dir, DecTreeGenerator.encode_blast(csv, dual_classifier), file, tree_type[i])
                if hsp_files[1].get() == 1:
                    csv = SeqGrabber.filter_csv(csv, file[0: len(file) - 4])
                    create_tree(non_dir, DecTreeGenerator.encode_blast(csv, classifier), file, tree_type[i])
            i += 1


# takes the dataframe data that has been created and turn it into a graphical representation of trees
def create_tree(dir, alt_csv, file, tree_type):
    csvGenerator.create_dir(os.path.join(png_dir, os.path.join(file[:len(file) - 4], dir)), tree_dir)
    csvGenerator.create_dir(os.path.join(key_dir, dir), tree_dir)
    csvGenerator.create_dir(os.path.join(dot_dir, os.path.join(file[:len(file) - 4], dir)), tree_dir)
    topics = []
    for topic in tree_type:
        topics.append(topic)
    DecTreeGenerator.build_tree(alt_csv, file, topics, dir)
    DecTreeGenerator.create_key(alt_csv, file, dir)
