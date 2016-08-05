import os
import subprocess

import matplotlib.pyplot as plt
import pandas as pd
from pandas.tools.plotting import table
from sklearn.tree import DecisionTreeClassifier, export_graphviz

csv_dir = "NRPSCSV"
dot_dir = "TreeDot"
png_dir = "TreePng"
ana_dir = "Analysis"
nrps_dir = "NRPS"
tree_dir = "Tree"
key_dir = "TreeKey"
hsp_name = "sequence"
non_name = "non-specific sequence"


# reads a csv file and returns it as a dataframe
def get_blast_data(csv):
    if os.path.exists(os.path.join(ana_dir, os.path.join(nrps_dir, os.path.join(csv_dir, csv)))):
        return pd.read_csv(os.path.join(ana_dir, os.path.join(nrps_dir, os.path.join(csv_dir, csv))), sep='^')


# encodes the names into a new target row of the csv dataframe and returns it
def encode_blast(csv, target):
    alt_csv = csv.copy()
    targets = alt_csv[target].unique()
    int_map = {name: n for n, name in enumerate(targets)}
    alt_csv["target"] = alt_csv[target].replace(int_map)
    return alt_csv


# builds a tre like build_tree but rather than passing it to show_tree to have a png exported it instead just returns
# the tree to the function  that called it
def build_tree_exc(alt_csv, factors):
    t = alt_csv["target"]
    f = alt_csv[factors]
    d_tree = DecisionTreeClassifier(min_samples_split=1, random_state=99, criterion='gini')
    d_tree.fit(f, t)
    return d_tree


# generates a tree using the dataframe that was created
def build_tree(alt_csv, file, factors, dir):
    t = alt_csv["target"]
    f = alt_csv[factors]
    d_tree = DecisionTreeClassifier(min_samples_split=1, random_state=99, criterion='gini')
    d_tree.fit(f, t)
    if dir[0] == "H":
        show_tree(d_tree, factors, file, alt_csv[hsp_name], dir)
    if dir[0] == "n":
        show_tree(d_tree, factors, file, alt_csv[non_name], dir)


# creates a png of the tree that was generated and places it in a tree directory
def show_tree(d_tree, factors, file, target, dir):
    with open(os.path.join(ana_dir, os.path.join(tree_dir, os.path.join(dot_dir, os.path.join(file[:len(file)-4],
                os.path.join(dir, file[:len(file)-4] + "-" + str(factors)[2:len(str(factors))-2] +
                    "-" + "_tree.dot"))))), 'w') as f:
        export_graphviz(d_tree, out_file=f, feature_names=factors, class_names=target, rounded=True)
    command = ["dot", "-Tpng", os.path.join(ana_dir, os.path.join(tree_dir, os.path.join(dot_dir,
                   os.path.join(file[:len(file)-4], os.path.join(dir, file[:len(file)-4] + "-" +
                       str(factors)[2:len(str(factors))-2] + "-" + "_tree.dot"))))), "-o", os.path.join(ana_dir,
                           os.path.join(tree_dir, os.path.join(png_dir, os.path.join(file[:len(file)-4],
                               os.path.join(dir, file[:len(file)-4] + "-" + str(factors)[2:len(str(factors))-2] +
                                   "-" + "_tree.png")))))]
    subprocess.check_call(command)


# creates a png of table key for the tree and places it in a key directory
def create_key(alt_csv, file, dir):
    fig, ax = plt.subplots(figsize=(66, len(alt_csv)/5.2))
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_frame_on(False)
    tabla = table(ax, alt_csv, loc='upper right', colWidths=[0.15] * len(alt_csv.columns))
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(5)
    tabla.scale(.8, .8)
    plt.savefig(os.path.join(ana_dir, os.path.join(tree_dir, os.path.join(key_dir, os.path.join(dir, file[:len(file)-4] + "_key.png")))),
                   transparent=True)