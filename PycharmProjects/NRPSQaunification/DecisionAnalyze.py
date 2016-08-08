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
def post_analyze(post_analysis, post_type, factors, samples):
    csv_files = []
    csvGenerator.simple_dir(post_dir)
    csvGenerator.create_dir(des_dir, post_dir)
    for [dirpath, dirname, filename] in os.walk(os.path.join(ana_dir, os.path.join(nrps_dir, csv_dir))):
        csv_files.extend(filename)
    for file in csv_files:
        if file[0:len(file) - 4] not in os.listdir(os.path.join(ana_dir, os.path.join(nrps_dir, csv_dir))) and file[
               0:len(file) - 4] in post_analysis:
            csv = DecTreeGenerator.get_blast_data(file)
            result = [[], []]
            if post_type[0].get() == 1 and post_type[1].get() == 0:
                result[0].append(predict_class(DecTreeGenerator.build_tree_exc(csv, factors), samples))
                f = open(os.path.join(ana_dir, os.path.join(post_dir, os.path.join(des_dir, os.path.join(
                        file[0:len(file) - 4], file[0:len(file) - 4] + "-" + "Class")))), "w")
                f.append("Name: " + file[0:len(file) - 4] + "\n")
                f.append("Type of Post-Analysis: Class" + "\n")
                f.append("Class: " + result[0] + "\n")
            elif post_type[1].get() == 1 and post_type[0].get() == 0:
                result.append(predict_prob(DecTreeGenerator.build_tree_exc(csv, factors), samples))
                f = open(os.path.join(ana_dir, os.path.join(post_dir, os.path.join(des_dir, os.path.join(
                        file[0:len(file) - 4], file[0:len(file)-4] + "-" + "Probabilities")))), "w")
                f.append("Name: " + file[0:len(file) - 4] + "\n")
                f.append("Type of Post-Analysis: Probabilities" + "\n")
                f.append("Probabilities: " + result[1] + "\n")
            elif post_type[0].get() == 1 and post_type[1].get() == 0:
                result.append(predict_prob(DecTreeGenerator.build_tree_exc(csv, factors), samples))
                f = open(os.path.join(ana_dir, os.path.join(post_dir, os.path.join(des_dir, os.path.join(
                        file[0: len(file) - 4], file[0:len(file) - 4] + "-" + "Class and Probabilities")))))
                f.append("Name: " + file[0:len(file) - 4] + "\n")
                f.append("Type of Post-Analysis: Both Class and Probabilities" + '\n')
                f.append("Class: " + result[0] + "\n")
                f.appned("Probabilities: " + result[1] + "\n")


# predict class value of a sample based on the Decision tree
def predict_class(d_tree, samples):
    return d_tree.predict(samples)


# predict class probability of a sample based on the Decision tree
def predict_prob(d_tree, samples):
    return d_tree.predict_prob(samples)




