import os

import pandas as pd

import DecTreeGenerator

ana_dir = "Analysis"
nrps_dir = "NRPS"
csv_dir = "NRPSCSV"
hsp_name = "sequence"
non_name = "non-specific sequence"


query = input("Search Query: (RootNRPS^Table Type^Target Code)\n")
if os.path.exists(os.path.join(ana_dir, os.path.join(nrps_dir, os.path.join(csv_dir, query[:query.index("^")] + ".csv")))):
    df = pd.read_csv(os.path.join(ana_dir, os.path.join(nrps_dir, os.path.join(csv_dir, query[:query.index("^")] + ".csv"))), sep='^')
    query = query[query.index("^") + 1:]
    df = DecTreeGenerator.encode_blast(df, query[:query.index("^")])
    values = df["target"]
    if query[:query.index("^")] == hsp_name:
        answer = df[hsp_name]
    elif query[:query.index("^")] == non_name:
        answer = df[non_name]
    i = 0
    for result in values:
        hat = query[query.index("^") + 1]
        if str(result) == query[query.index("^") + 1:]:
            print(str(result) + ":" + answer[i] + '\n')
