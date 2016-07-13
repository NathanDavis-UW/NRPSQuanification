from Bio.Blast import NCBIXML

#record = SeqIO.read("rootNRPS", format="fasta")
#result_handle = NCBIWWW.qblast("blastn", "nt", record.seq)
#save_file = open("my_blast.xml", "w")
#save_file.write(result_handle.read())
#save_file.close()
#result_handle.close()
result_handle = open("my_blast.xml")
blast_record = NCBIXML.read(result_handle)
i = 0
for alignment in blast_record.alignments:
    for hsp in alignment.hsps:
        i += 1
        f = open("result" + str(i), 'w')
        f.write('sequence:' + str(alignment.title) +'\n')
        f.write('length:' + str(alignment.length) + '\n')
        f.write(str(hsp.query[0:len(hsp.sbjct)]) + '\n')
        f.write(str(hsp.match[0:len(hsp.sbjct)]) + '\n')
        f.write(str(hsp.sbjct[0:len(hsp.sbjct)]) + '\n')