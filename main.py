from psychopy import visual, core, event,gui
from random import shuffle
from helpers import get_subject_info
import training, testing, memory

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


def main():
    new_experiment, subject_number = startup()
    names = get_names(new_experiment)

    round_num, dom_eye = get_subject_info(training = True,
                                          subject_number = subject_number)


    window = visual.Window([1680,1050],
                          monitor = "testMonitor",
                          units = "pix",
                          rgb=(-1,-1,-1),
                          fullscr = True)

    training.main(window, new_experiment, names, subject_number, round_num, dom_eye)
    testing.main(window, new_experiment, subject_number)
    memory.main(window, new_experiment, 1)
    window.close()


if __name__ == '__main__':
    main()
