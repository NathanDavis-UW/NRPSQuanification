from sklearn.tree import DecisionTreeClassifier
import DecTreeGenerator
import os
import csvGenerator
ana_dir = "Analysis"
nrps_dir = "NRPS"
csv_dir = "NRPSCSV"
post_dir = "Post-Analysis"
des_dir = "Decision Tree Results"

# This is a functiont that does certain statistics calculations that require a decision tree
def post_analyze(post_analysis, post_type):
    csv_files = []
    csvGenerator.simple_dir(post_dir)
    csvGenerator.create_dir(des_dir, post_dir)
    for [dirpath, dirname, filename] in os.walk(os.path.join(ana_dir, os.path.join(nrps_dir, csv_dir))):
        csv_files.extend(filename)
    for file in csv_files:
        if file[0:len(file) - 4] not in os.listdir(os.path.join(ana_dir, os.path.join(nrps_dir, csv_dir))) and file[
            0:len(file) - 4] in post_analysis:
            csv = DecTreeGenerator.get_blast_data(file)
            if post_type[0] == 1:


