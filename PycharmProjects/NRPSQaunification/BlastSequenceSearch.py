import os

from Bio import SeqIO
from Bio.Blast import NCBIXML

import BLASTWriter
import BLASTExecute


# creates all the directories and info files in the blast section of the analysis
def get_sequences(blast_analysis):
    # statement of constants
    ana_dir = "Analysis"
    bla_dir = "BLAST"
    BLASTWriter.simple_dir(bla_dir)
    root_dir = "NRPSRoot"
    xml_dir = "BLASTXML"
    BLASTWriter.create_dir(xml_dir, bla_dir)
    stan_dir = "BLASTStandard"
    BLASTWriter.create_dir(stan_dir, bla_dir)
    fas_dir = "BLASTFASTA"
    Sraw_dir = "BLASTStandardRaw"
    main_dir = []
    Fraw_dir = "BLASTFASTARaw"

    for arr in os.walk(root_dir):
        main_dir.extend(arr[2])
    for file in main_dir:
        if file[0:len(file)-4] not in os.listdir(os.path.join(ana_dir, os.path.join(bla_dir, stan_dir))) and file[0:len(file)-4] in blast_analysis:
            record = SeqIO.read(os.path.join(root_dir, file), format="gb")
            if ("BLAST-" + file[0:len(file)-4] + ".xml") not in os.listdir(os.path.join(ana_dir, os.path.join(bla_dir, xml_dir))):
                BLASTExecute.blast_execute(record)
            result_handle = open(os.path.join(ana_dir, os.path.join(bla_dir, os.path.join(xml_dir, "BLAST-" + record.name + ".xml"))))
            blast_record = NCBIXML.read(result_handle)
            k = 0
            e_threshold = pow(10, -25)
            rec_dir = record.name
            # creates all the directories that are needed that have not been made already
            BLASTWriter.create_dir(os.path.join(stan_dir, rec_dir), bla_dir)
            BLASTWriter.create_dir(Sraw_dir, bla_dir)
            BLASTWriter.create_dir(os.path.join(Sraw_dir, rec_dir), bla_dir)
            BLASTWriter.create_dir(os.path.join(fas_dir, rec_dir), bla_dir)
            BLASTWriter.create_dir(Fraw_dir, bla_dir)
            BLASTWriter.create_dir(os.path.join(Fraw_dir, rec_dir), bla_dir)

            # goes through all the alingments that were found in the BLAST Search and creates files for them within the
            # Analysis/BLAST file system
            for alignment in blast_record.alignments:
                k += 1
                i = 0
                al_dir = alignment.title[:alignment.title.index(" ")]
                BLASTWriter.create_dir(os.path.join(stan_dir, os.path.join(rec_dir, al_dir)), bla_dir)
                BLASTWriter.create_dir(os.path.join(fas_dir, os.path.join(rec_dir, al_dir)), bla_dir)
                BLASTWriter.write_full_standard(k, alignment, record)
                for hsp in alignment.hsps:
                    if hsp.expect < e_threshold:
                        i += 1
                        BLASTWriter.create_blast_files(open(os.path.join(ana_dir, os.path.join(bla_dir,
                                                           os.path.join(stan_dir, os.path.join(rec_dir,
                                                               os.path.join(alignment.title[:alignment.title.index(" ")],
                                                                   alignment.title[:alignment.title.index(" ")]
                                                                       + "-" + str(i) + "-hsp"))))), 'w'),
                                                                           BLASTWriter.write_blast_standard(i,
                                                                               alignment, hsp, rec_dir))
                        BLASTWriter.create_blast_files(open(os.path.join(ana_dir, os.path.join(bla_dir,
                                                           os.path.join(Sraw_dir, os.path.join(rec_dir,
                                                               alignment.title[:alignment.title.index(" ")] + "-" +
                                                                   str(i) + "-hsp")))), 'w'),
                                                                       BLASTWriter.write_blast_standard(i, alignment,
                                                                           hsp, rec_dir))
                        BLASTWriter.create_blast_files(open(os.path.join(ana_dir, os.path.join(bla_dir,
                                                           os.path.join(fas_dir, os.path.join(rec_dir,
                                                               os.path.join(alignment.title[:alignment.title.index(" ")],
                                                                   alignment.title[:alignment.title.index(" ")] + "-"
                                                                       + str(i) + "-hsp"))))), 'w') ,
                                                                           BLASTWriter.write_blast_fasta(i, alignment,
                                                                               hsp, rec_dir))
                        BLASTWriter.create_blast_files(open(os.path.join(ana_dir, os.path.join(bla_dir,
                                                           os.path.join(Fraw_dir, os.path.join(rec_dir,
                                                               alignment.title[:alignment.title.index(" ")] + "-" +
                                                                   str(i) + "-hsp")))), 'w'),
                                                                       BLASTWriter.write_blast_fasta(i, alignment,
                                                                           hsp, rec_dir))