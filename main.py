from psychopy import visual, core, event,gui
from random import shuffle
import training

"""
Main experimental harness
"""

def startup():

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

def main():
    new_experiment, subject_number = startup()
    names = get_names(new_experiment)
    training.main(new_experiment, names, subject_number)

if __name__ == '__main__':
    main()
