from psychopy import visual, core, gui
from random import sample
from helpers import choose_pair
import csv
import ast

def get_subject_info():
    """
    Gets subject info and returns it as a dict
    """
    #TODO: What information is needed?

    subject_info = {
                    'Subject number': ''
                    }
    dlg = gui.DlgFromDict(dictionary = subject_info, title = "Subject info")
    return subject_info


def retrieve_subject_pairs(subject_number):
    """
    Given the subject number, retrieves which pairs they saw from results.csv
    """
    subjects = []
    with open('results.csv', 'rb') as f:
        reader = csv.reader(f)
        subjects = list(reader)

    #remove header list
    subjects = subjects[1:]

    for subject in subjects:
        if int(subject[0]) == subject_number:
            pairs = ast.literal_eval(subject[1])
            return pairs


def main():
    subject_info = get_subject_info()
    chosen_pairs = retrieve_subject_pairs(int(subject_info['Subject number']))
    for i in chosen_pairs:
        pair_path = choose_pair(i)


if __name__ == "__main__":
    main()
