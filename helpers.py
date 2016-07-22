import csv
import ast

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
