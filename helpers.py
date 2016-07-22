from psychopy import gui
import csv
import ast

def get_subject_info(training = False):
    """
    Retrieves subject information

    The optional 'training' parameter, if True, asks for the number of pairs
    to show as well.

    Returns either a tuple of subject number and number of pairs, or just
    the subject number
    """
    #TODO: Eliminate asking for number of pairs
    #TODO: Dominant eye?


    if training:
        window_title = "Training"
    else:
        window_title = "Enter subject number"

    input = gui.Dlg(title = window_title)
    input.addField('Subject Number')
    if training:
        input.addField('Number of pairs')

    input.show()

    if training:
        return (int(input.data[0]), int(input.data[1]))
    else:
        return int(input.data[0])


def choose_pair(i):
    """
    Returns path to the pair
    """

    return "Pairs/Pair " + str(i) +"/"


def retrieve_subject_pairs(subject_number):
    """
    Given the subject number, retrieves which pairs they saw from results.csv
    and the names

    returns a tuple (pair numbers, image names)
    """

    subjects = read_csv('training_results.csv')

    for subject in subjects:
        if int(subject[0]) == subject_number:
            pairs = ast.literal_eval(subject[1])
            names = ast.literal_eval(subject[2])
            return (pairs, names)


def read_csv(filename):
    """
    Reads a csv and returns a list of lists with csv data, ignoring the header
    """

    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        data = list(reader)

    return data[1:]
