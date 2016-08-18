from sklearn.tree import DecisionTreeClassifier
import DecTreeGenerator
import os
import csvGenerator
import SeqGrabber
ana_dir = "Analysis"
nrps_dir = "NRPS"
bla_dir = "BLAST"
Sraw_dir = "BLASTStandardRaw"
csv_dir = "NRPSCSV"
post_dir = "Post-Analysis"
des_dir = "Decision Tree Results"
classifier = "NRPS Classifier"
dual_classifier = "NRPS-PKS Classifier"


# This is a functiont that does certain statistics calculations that require a decision tree
def post_analyze(post_analysis, post_type, factors, samples):
    csv_files = []
    csvGenerator.simple_dir(post_dir)
    csvGenerator.create_dir(des_dir, post_dir)
    for [dirpath, dirname, filename] in os.walk(os.path.join(ana_dir, os.path.join(nrps_dir, csv_dir))):
        csv_files.extend(filename)
    for file in csv_files:
        if file[0:len(file) - 4] not in os.listdir(os.path.join(ana_dir, os.path.join(nrps_dir, csv_dir))) and \
               file in post_analysis:
            sample = open(os.path.join(ana_dir, os.path.join(bla_dir, os.path.join(Sraw_dir, os.path.join(
                             file[0:len(file)-4], samples.get() + "-hsp")))))
            spl = get_data(sample, factors)
            csv = DecTreeGenerator.get_blast_data(file)
            csv = SeqGrabber.filter_csv(csv, file[0: len(file) - 4])
            csv = DecTreeGenerator.encode_blast(csv, classifier)
            result = [[], []]
            if post_type[0].get() == 1 and post_type[1].get() == 0:
                result[0].append(predict_class(DecTreeGenerator.build_tree_exc(csv, factors), spl))
                f = open(os.path.join(ana_dir, os.path.join(post_dir, os.path.join(des_dir, os.path.join(
                        file[0:len(file) - 4], file[0:len(file) - 4] + "-" + "Class")))), "w")
                f.write("Name: " + file[0:len(file) - 4] + "\n")
                f.write("Type of Post-Analysis: Class" + "\n")
                f.write("Class: " + str(result[0]) + "\n")
            elif post_type[1].get() == 1 and post_type[0].get() == 0:
                result.append(predict_prob(DecTreeGenerator.build_tree_exc(csv, factors), spl))
                f = open(os.path.join(ana_dir, os.path.join(post_dir, os.path.join(des_dir, os.path.join(
                        file[0:len(file) - 4], file[0:len(file)-4] + "-" + "Probabilities")))), "w")
                f.write("Name: " + file[0:len(file) - 4] + "\n")
                f.write("Type of Post-Analysis: Probabilities" + "\n")
                f.write("Probabilities: " + str(result[1]) + "\n")
            elif post_type[0].get() == 1 and post_type[1].get() == 0:
                result.append(predict_prob(DecTreeGenerator.build_tree_exc(csv, factors), spl))
                f = open(os.path.join(ana_dir, os.path.join(post_dir, os.path.join(des_dir, os.path.join(
                        file[0: len(file) - 4], file[0:len(file) - 4] + "-" + "Class and Probabilities")))))
                f.write("Name: " + file[0:len(file) - 4] + "\n")
                f.write("Type of Post-Analysis: Both Class and Probabilities" + '\n')
                f.write("Class: " + str(result[0]) + "\n")
                f.write("Probabilities: " + str(result[1])
                         + "\n")


# predict class value of a sample based on the Decision tree
def predict_class(d_tree, samples):
    return d_tree.predict(samples)


# predict class probability of a sample based on the Decision tree
def predict_prob(d_tree, samples):
    return d_tree.predict_prob(samples)


# gets data from a standard BLAST file to be used in post tree analysis
def get_data(sample, factors):
    spl = [[], []]
    fil = sample.readlines()
    spl[0].append(fil[0][10:])
    i = 0
    for sp in fil[1:len(fil)-3]:
        if sp[:sp.index(":")] in factors:
            i += 1
            spl[1].append(sp[len(factors[i])+1:])
    return spl