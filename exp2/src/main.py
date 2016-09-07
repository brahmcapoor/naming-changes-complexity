from psychopy import gui, logging
import os
import shutil


def startup():
    """
    Gets various startup config options, and returns a tuple of whether it is a
    new experiment and what the subject number, round number and dominant eye
    are.
    """

    check = gui.Dlg("Startup")
    check.addField("Starting over?", False)
    check.addField("Subject Number", 1)
    check.addField('Round Number', 1)
    check.addField('Right eye dominant', True)
    check.show()

    return tuple(check.data)


def setup_files():
    """
    Clears the csv results files
    """
    if os.path.exists("../subject_logs"):
        shutil.rmtree("../subject_logs")

    os.mkdir("../subject_logs")


def main():
    # get basic experiment info
    new_experiment, subject_number, round_num, dom_eye = startup()

    if new_experiment():
        setup_files()

    with open("../names.txt") as f:
        names =

if __name__ == '__main__':
    main()
