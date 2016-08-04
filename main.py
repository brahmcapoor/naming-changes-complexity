from psychopy import visual, core, event,gui
from random import shuffle, randint
from helpers import get_subject_info, read_csv, choose_pair
from experiment_objects import Image, ImagePair, Trial
import training, testing, memory, os, csv

"""
Main experimental harness
"""

def startup():
    """
    Gets various startup config options, and returns a tuple of whether it is a
    new experiment and what the subject number is.
    """

    check = gui.Dlg("New experiment?")
    check.addField("Starting over?", False)
    check.addField("Subject Number", 1)
    check.show()

    return tuple(check.data)

def get_names(new_experiment = False):
    """
    Reads a list of names from names.txt, writes them into a list, and
    shuffles the list

    if new_experiment is true, shuffles the names array before returning
    """

    with open('names.txt', 'rb') as f:
        names = f.read().splitlines()
    #shuffle before each experiment begins
    if new_experiment:
        shuffle(names)
        with open('names.txt', 'wb') as f:
            f.writelines(name + '\n' for name in names)

    return names

def get_chosen_pairs():
    """
    Returns all the pair numbers that have already been chosen
    """
    data = read_csv('training_results.csv')
    return [subject[3] for subject in data]

def setup_files():
    """
    Clears the csv results files
    """
    if os.path.isfile("training_results.csv"):
        os.remove("training_results.csv")
    if os.path.isfile("testing_results.csv"):
        os.remove("testing_results.csv")

    with open("training_results.csv", 'wb') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_ALL)

        header = ["Subject Number", "Round Number", "Dominant Eye",
                  "Pair Number", "Name 1", "Name 2"]
        wr.writerow(header)


    open("testing_results.csv", 'w').close()


def main():
    new_experiment, subject_number = startup()

    if new_experiment:
        setup_files()

    names = get_names(new_experiment)

    round_num, dom_eye = get_subject_info(training = True,
                                          subject_number = subject_number)

    chosen_pairs = get_chosen_pairs()

    pair_num = None
    name_pair = None

    if subject_number % 2 != 0 or round_num != 1:
        while True:
            pair_num = randint(1,8)
            if str(pair_num) not in chosen_pairs:
                break
        pair_path = choose_pair(pair_num)
        name_pair = names[randint(1,8)]
        name_pair = name_pair.split(" ")

    else:
        last_subject = retrieve_subject_info(subject_number - 1)
        pair_num = last_subject[3]
        pair_path = choose_pair(pair_num)
        name_pair = [last_subject[5], last_subject[4]]


    window = visual.Window([1680,1050],
                          monitor = "testMonitor",
                          units = "pix",
                          rgb=(-1,-1,-1),
                          fullscr = True)

    subject_image_pair = ImagePair(pair_path, name_pair)
    trial = Trial(subject_number, round_num, dom_eye, subject_image_pair,
                  pair_num)

    training.main(window, trial)
    testing.main(window, trial)
    memory.main(window, new_experiment, 1)
    window.close()


if __name__ == '__main__':
    main()
