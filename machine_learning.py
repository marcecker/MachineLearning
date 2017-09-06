from database import balloons_adult_and_stretch as db
from optparse import OptionParser
import os


def parse_arguments():
    parser = OptionParser()

    parser.add_option("-a", "--add-training-data", dest="trainings_data",
        help="Path to a csv file containing trainings_data")
    parser.add_option("-t", "--training", action="store_true", dest="training",
        default=False, help="This flag starts the training on the dataset")

    (options, args) = parser.parse_args()

    verify_options(options, parser)

    return options


def verify_options(options, parser):
    if options.trainings_data and options.training:
        parser.error("It is not allowed to use more than one flag out of [-a, -t]")

    if not options.trainings_data and not options.training:
        parser.error("At least one flag out of [-a, -t] must be selected")

    if options.trainings_data and not os.path.isfile(options.trainings_data):
        parser.error("Invalid file path {}".format(options.trainings_data))


if __name__ == "__main__":
    options = parse_arguments()
    if options.trainings_data:
        db.add_trainings_data_csv(options.trainings_data)

    else:
        print(db.benchmark())
