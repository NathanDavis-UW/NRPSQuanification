import os
import pandas as pd

from Bio import Entrez

search_database = 'nucleotide'
Entrez.email = 'n.j.davis.college@gmail.com'
nrps_dir = "NRPS"
seq_dir = "NRPSSequences"
ana_dir = "Analysis"

# list of all of the experimentally verified nrps
nrps_arr = ["EF601124", "EF672686", "AM990467", "AM231618", "AY787762", "AB101202", "AB070952", "AB070955", "AB070950",
            "AF074705", "AB070951", "AB211309", "AB366635", "AB375771", "AF007865", "AF034152", "AF143772", "AF286216",
            "AF386507", "AF512431", "AH012634", "AJ488769", "AJ605139", "AM071396", "AM113472", "AM231612", "AM712657",
            "AY048670", "AY061859", "AY167420", "AY192157", "AY263398", "AY541063", "AY588942", "AY735112", "AY838877",
            "DQ075244", "DQ118863", "DQ151887", "DQ174261", "DQ192518", "DQ360825", "DQ403252", "DQ837301", "EF125025",
            "EF210776", "EF429247", "EF472579", "EF484930", "EU074211", "EU195114", "EU199080", "EU199081", "EU670723",
            "EU874252", "EU874252", "FJ609416", "FJ768674", "FJ768957", "FN545130", "GQ331953", "GQ370384", "GQ869385",
            "GU174493", "HM038106", "DD163071", "DI166456", "DI166763", "EU088199", "FR727736", "HQ668144", "JN634585",
            "KF301601", "HQ668144", "AJ011849", "X70356", "D50308", "X61658", "AF004835", "HM855229", "AB684619",
            "FN563143", "U95370", "AJ632270"]

# list of all the experimentally verifed nrps/pks hybrids
hybrid_arr = ["BN001209", "AJ561198", "U82965", "Y16952", "HQ679900", "AF184956", "AF484556", "AJ586576", "AJ634060",
              "AY328023", "DQ013294", "EF552687", "AM411073", "DD174030", "AB050629", "AM411073", "AJ576102",
              "AJ874112", "AL009126", "AB283030", "FJ823461", "GU479979", "FJ809786", "GQ979609", "AY522504",
              "AY652953", "HQ696500", "AM746336", "DQ065771", "EF397502", "AY700570", "FN433113", "AJ441056",
              "AM990466", "DQ019316", "AF183408", "AM231619", "AM229678", "AJ698723", "AJ698723", "AF188287",
              "AF188287", "AB070956", "AB070942", "AB279593", "AF155773", "AF204805", "AF210249", "AF210843",
              "AF217189", "AF235504", "AF319998", "AF516145", "AJ557546", "AJ699306", "AM179409", "AM231613",
              "AM236324", "AM409327", "AM779763", "AM946600", "AM988861", "AY212249", "AY271660", "AY439015",
              "AY553235", "AY834753", "AY974560", "DQ176871", "DQ351275", "DQ885223", "EF028635", "EF032505",
              "EF159954", "EU240558", "EU364530", "EU414841", "EU449979", "EU603720", "FJ430564", "GQ176852",
              "GU063811", "GU385216", "X86780", "Y12527", "HQ696501", "AF082100", "HE575208", "HE616533", "FN547928",
              "GQ166664", "X65195"]

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


# Analyzes A csv to see if the included proteins are experimentally known nrpss based on a comparison of accension codes
# from the nrps_arr list
def filter_csv(alt_csv, file):
    dp_name = []
    dp_arr = []
    p_name = []
    p_arr = []
    for dp in alt_csv["non-specific sequence"]:
        f = open(os.path.join(ana_dir, os.path.join(nrps_dir, os.path.join(seq_dir, os.path.join(file,
                    "NRPSGeneralInfo_" + dp[3:dp[3:len(dp) - 1].index("|")+3] + ".gbk")))), 'r')
        count = len(dp_arr)
        for s in f.readlines():
            cat = s[11:len(s)-1]
            if s[0:9] == "ACCESSION" and (s[12:len(s)-1]) in hybrid_arr:
                dp_arr.append(2)
                dp_name.append("NRPS-PKS Hybrid")
                p_arr.append(1)
                p_name.append("NRPS")
                break
            elif s[0:9] == "ACCESSION" and (s[12:len(s)-1]) in nrps_arr:
                p_arr.append(1)
                p_name.append("NRPS")
                dp_arr.append(1)
                dp_name. append("NRPS")
                break
            elif s[0:9] == "ACCESSION":
                dp_arr.append(0)
                dp_name.append("NRPS")
                p_name.append("Non-NRPS")
                p_arr.append(0)
                break
        if count == len(dp_arr):
            dp_arr.append(0)
            dp_arr.append(0)
            dp_name.append("NRPS")
            p_name.append("Non-NRPS")
        print(str(dp_arr))
    alt_csv["NRPS Classifier"] = pd.Series(p_arr, index=alt_csv.index)
    alt_csv["NRPS-PKS Classifier"] = pd.Series(dp_arr, index=alt_csv.index)
    alt_csv["NRPS Classifier Name"] = pd.Series(p_name, index=alt_csv.index)
    alt_csv["NRPS-PKS Classifier Name"] = pd.Series(dp_name, index=alt_csv.index)
    return alt_csv


