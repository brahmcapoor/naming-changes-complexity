from psychopy import visual, gui, event
from psychopy.visual import TextStim
import csv
import ast

def get_subject_info(training = False, subject_number = 1):
    """
    Retrieves subject information

    The optional 'training' parameter, if True, asks for the number of pairs
    to show as well.

    Returns either a list of information, or just
    the subject number
    """

    window_title = "Subject " + str(subject_number)

    input = gui.Dlg(title = window_title)
    input.addField('Round number', 1)
    input.addField("Right eye dominant", True)
    input.show()

    if training:
        return tuple(input.data)
    else:
        return int(input.data[0])


def choose_pair(i):
    """
    Returns path to the pair
    """

    return "Pairs/Pair " + str(i) +"/"


def retrieve_subject_info(subject_number):
    """
    Given the subject number, retrieves which pairs they saw from training_results.csv
    and the names

    returns a tuple representing the subject
    """

    subjects = read_csv('training_results.csv')

    for subject in subjects:
        if int(subject[0]) == subject_number:
            return tuple(subject)


def read_csv(filename):
    """
    Reads a csv and returns a list of lists with csv data, ignoring the header
    """

    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        data = list(reader)

    return data[1:]


def get_user_input(window, position, fontsize = 50):

    input_name = ""
    user_input = TextStim(win = window,
                          text = input_name,
                          pos = position,
                          height = fontsize)

    user_input.setAutoDraw(True)
    window.flip()

    while True:
        char = event.waitKeys()[0]
        if char.isalpha() and len(char) == 1:
            input_name += char
        if char ==  'return':
            user_input.setAutoDraw(False)
            window.flip()
            return input_name
        if char == 'comma':
            input_name = input_name[:-1]


        user_input.text = input_name
        window.flip()
