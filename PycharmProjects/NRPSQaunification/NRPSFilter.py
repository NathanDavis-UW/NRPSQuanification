import os

from Bio import SeqIO


def nrps_filterer(i_d, module_type):
    gen_b = 'NRPS' + module_type + 'Info_' + i_d
    for record in SeqIO.parse(open(gen_b, 'r'), 'genbank'):
        if not record.Division == 'PRN' or record.Division == 'BCT' or record.Division == 'PHG':
            f = open(gen_b, 'w')
            os.remove(str(f))


def genbank_indexer(record, feature_type, qualifier):
    index = dict()
    for (spot, feature) in enumerate(record.features):
        if feature.type == feature_type:
            if qualifier in feature.qualifiers:
                for value in feature.qualifiers[qualifier]:
                    if value in index:
                        print
                        'duplicate key %s has %i and %i' \
                        % (value, index[value], spot)
                    else:
                        index[value] = spot
    return index
