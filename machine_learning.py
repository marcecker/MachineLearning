from optparse import OptionParser
from classifiers.naive_bayes_classifier import NaiveBayesClassifier
import pandas as pd
import json

def parse_arguments():
    parser = OptionParser()
    parser.add_option("-d", "--datafile", action="store", type="string", dest="datafile")
    parser.add_option("-n", "--namefile", action="store", type="string", dest="namefile")
    parser.add_option("-c", "--class-key", action="store", type="string", dest="class_key", default="class")

    (options, args) = parser.parse_args()

    if not options.datafile:
        parser.error("-d (--datafile) is required")

    if not options.namefile:
        parser.error("-n (--namefile) is required")

    return options

if __name__ == "__main__":
    options = parse_arguments()
    names = list(pd.read_csv(options.namefile).columns.values)
    dataset = pd.read_csv(options.datafile, names=names)

    classifier = NaiveBayesClassifier(names, dataset, options.class_key)
    print(classifier.benchmark())
