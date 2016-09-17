from psychopy import visual, event, gui
from psychopy.visual import TextStim
from random import shuffle, randint
from experiment_objects import Image, ImagePair, Trial
import training
import testing
import memory
import practice
import os
import csv
import name_gen
import shutil

"""
Main experimental harness. Unless you're changing the sections of the
experiments, you shouldn't have to mess with this too much
"""


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


def get_names(new_experiment=False):
    """
    Reads a list of names from names.txt, writes them into a list, and
    shuffles the list

    if new_experiment is true, shuffles the names array before returning
    """

    with open('names.txt', 'rb') as f:
        names = f.read().splitlines()
    # shuffle before each experiment begins
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
    with open("training_results.csv", 'wb') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)

        header = ["Subject Number", "Round Number", "Dominant Eye",
                  "Pair Number", "Name 1", "Name 2"]
        wr.writerow(header)

    with open("memory_results_before.csv", 'wb') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        header = ["Subject Number", "Round Number", "Name 1",
                  "Remembered Name 1", "Name 2", "Remembered Name 2",
                  "Foil Name 1", "Foil Name 2"]
        wr.writerow(header)

    with open("memory_results_after.csv", 'wb') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        header = ["Subject Number", "Round number", "Name 1",
                  "Remembered Name 1", "Name 2", "Remembered Name 2",
                  "Foil Name 1", "Foil Name 2"]
        wr.writerow(header)

    if os.path.exists("subject logs"):
        shutil.rmtree("subject logs")

    os.makedirs("subject logs")

    with open('subject logs/catch trials.csv', 'wb') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)

        header = ["Subject Number", "Visible seen (should be > 14)", "Invisible \
                  seen (should be < 2)", "Invalid Trials"]
        wr.writerow(header)


def end_section(window, experiment_end=False):
    """
    After each section, press space to continue
    """

    if experiment_end:
        string = "End of experiment. Thank you!"
    else:
        string = "End of section"
    text = TextStim(win=window,
                    text=string,
                    pos=(0, 0),
                    alignHoriz='center',
                    alignVert='center',
                    height=50)

    text.draw()
    window.flip()
    event.waitKeys()
    window.flip()


def retrieve_subject_info(subject_number):
    """
    Given the subject number, retrieves which pairs they saw from
    training_results.csv and the names

    returns a tuple representing the subject
    """

    subjects = read_csv('training_results.csv')

    for subject in reversed(subjects):
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


def choose_pair(i):
    """
    Returns path to the pair
    """
    return "Pairs/Pair " + str(i) + "/"


def main():

    # get basic experiment info
    new_experiment, subject_number, round_num, dom_eye = startup()

    if new_experiment:
        # delete all existing results files and shuffle names
        setup_files()
        name_gen.main()

    names = get_names(new_experiment)

    pair_num = None
    name_pair = None

    if subject_number % 2 != 0 or round_num != 1:
        # new images and names need to be chosen
        pair_num = randint(1, 8)
        pair_path = choose_pair(pair_num)
        name_num = randint(0, 7)
        name_pair = names[name_num].split(" ")  # return a list of both names

    else:
        # get the images and names used by the last, odd-numbered subject
        last_subject = retrieve_subject_info(subject_number - 1)
        pair_path = choose_pair(last_subject[3])
        name_pair = [last_subject[5], last_subject[4]]

    # set up the psychopy window. Some params may need to be changed here if
    # changing the display. Creates a full screen, black window
    window = visual.Window([1680, 1050],
                           monitor="testMonitor",
                           units="pix",
                           rgb=(-1, -1, -1),
                           fullscr=True)

    # practice rounds
    practice.main(window, dom_eye)

    # subject_image_pair and trial are just objects which store a bunch of
    # information about the trial that's transferred to the various parts
    # of the experiment
    subject_image_pair = ImagePair(pair_path, name_pair)
    trial = Trial(window, subject_number, round_num, dom_eye,
                  subject_image_pair, pair_num)

    # set up a list of pairs and names already chosen so that if we need to
    # rechoose, we choose different ones.
    chosen_pairs = [pair_num]
    chosen_names = [name_pair]

    while True:
        # continue training and memory test until the memory task is passed
        end_section(window)
        training.main(trial)
        end_section(window)
        if memory.main(trial):
            # passed the memory test
            break
        else:
            # reset! Restart training and memory
            round_num = trial.round_number + 1
            while True:
                # choose new images and names
                pair_num = randint(1, 8)
                name_num = randint(0, 7)
                name_pair = names[name_num].split(" ")
                if pair_num not in chosen_pairs and name_pair not in \
                        chosen_names:
                    break
                chosen_pairs.append(pair_num)
                chosen_names.append(name_pair)

            pair_path = choose_pair(pair_num)

            # update the subject_image_pair and trial
            subject_image_pair = ImagePair(pair_path, name_pair)
            trial = Trial(window, subject_number, round_num, dom_eye,
                          subject_image_pair, pair_num)

    end_section(trial.window)
    testing.main(trial)
    end_section(trial.window)
    memory.main(trial, True)
    end_section(trial.window, True)
    window.close()


if __name__ == '__main__':
    main()
