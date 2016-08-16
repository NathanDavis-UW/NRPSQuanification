import os

# statement of constants
root_dir = "NRPSRoot"
csv_dir = "NRPSCSV"
Sraw_dir = "BLASTStandardRaw"
ana_dir = "Analysis"
tree_dir = "Tree"
nrps_dir = "NRPS"
bla_dir = "BLAST"


# creates csv files from blast standard info files and places them in a csv directory
def create_csv(tree_analysis):
    create_dir(csv_dir, nrps_dir)
    main_dir = []
    for arr in os.walk(root_dir):
        main_dir.extend(arr[2])
    for file in main_dir:
        if file[0:len(file)-4] in tree_analysis:
            # this defines all the columns of the csv file
            f = open(os.path.join(ana_dir, os.path.join(nrps_dir, os.path.join(csv_dir, file[:len(file)-4] + ".csv"))), 'w')
            f.write("sequence^")
            f.write("non-specific sequence^")
            f.write("length^")
            f.write("description^")
            f.write("weighted e value^")
            f.write("score^")
            f.write("adjusted score^")
            f.write("e value" + '\n')

            # this fills all the the columns of the csv file
            sub_dir = []
            for arr in os.walk(os.path.join(ana_dir, os.path.join(bla_dir, os.path.join(Sraw_dir, file[:len(file)-4])))):
                sub_dir.extend(arr[2])
            for fil in sub_dir:
                sub_f = open(os.path.join(ana_dir, os.path.join(bla_dir, os.path.join(Sraw_dir, os.path.join(file[:len(file)-4], fil)))), 'r')
                Sf_text = sub_f.readlines()
                f.write(Sf_text[0][10:len(Sf_text[0])-1] + "^")
                f.write(Sf_text[0][10:Sf_text[0].index("-")] + "^")
                f.write(Sf_text[1][8:len(Sf_text[1])-1] + "^")
                f.write(Sf_text[2][13:len(Sf_text[2])-1] + "^")
                f.write(Sf_text[4][12:len(Sf_text[4])-1] + "^")
                f.write(Sf_text[5][7:len(Sf_text[5])-1] + "^")
                f.write(Sf_text[6][16:len(Sf_text[6])-1] + "^")
                f.write(Sf_text[3][3:len(Sf_text[3])-1] + '\n')


# creates a directory that does sit inside a non-major sub-directory
def create_dir(file, dir):
    if not os.path.exists(os.path.join(ana_dir, os.path.join(dir, file))):
        os.makedirs(os.path.join(ana_dir, os.path.join(dir, file)))


# creates a directory that does not sit inside a non-major sub-directory
def simple_dir(d):
    if not os.path.exists(os.path.join(ana_dir, d)):
        os.makedirs(os.path.join(ana_dir, d))