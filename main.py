from psychopy import visual, core, event, gui
from psychopy.visual import TextStim
from random import shuffle, randint
from helpers import get_subject_info, read_csv, choose_pair
from experiment_objects import Image, ImagePair, Trial
import training, testing, memory, os, csv, name_gen, shutil

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
    with open("training_results.csv", 'wb') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)

        header = ["Subject Number", "Round Number", "Dominant Eye",
                  "Pair Number", "Name 1", "Name 2"]
        wr.writerow(header)

    with open("testing_results.csv", 'wb') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)

        header = ["Subject Number",  "Individual results", "Image 1 Average", "Image 2 Average", "Names"]

        wr.writerow(header)

    with open("memory_results_before.csv", 'wb') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        header = ["Subject Number", "Round Number", "Name 1", "Remembered Name 1", "Name 2", "Remembered Name 2", "Foil Name 1", "Foil Name 2"]
        wr.writerow(header)

    with open("memory_results_after.csv", 'wb') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        header = ["Subject Number", "Round number", "Name 1", "Remembered Name 1", "Name 2", "Remembered Name 2", "Foil Name 1", "Foil Name 2"]
        wr.writerow(header)

    if os.path.exists("subject logs"):
        shutil.rmtree("subject logs")

    os.makedirs("subject logs")

    with open('subject logs/catch trials.csv', 'wb') as f:
        wr = csv.writer(f, quoting = csv.QUOTE_NONNUMERIC)

        header = ["Subject Number", "Visible seen (should be > 14)", "Invisible seen (should be < 2)"]
        wr.writerow(header)

def end_section(window, experiment_end = False):
    """
    After each section, press space to continue
    """

    if experiment_end:
        string = "End of experiment. Thank you!"
    else:
        string = "End of section"
    text= TextStim(win = window,
                    text = string,
                    pos = (0,0),
                    alignHoriz = 'center',
                    alignVert = 'center',
                    height = 50)

    text.draw()
    window.flip()
    event.waitKeys()
    window.flip()

def main():
    new_experiment, subject_number = startup()

    if new_experiment:
        setup_files()
        name_gen.main()

    names = get_names(new_experiment)

    round_num, dom_eye = get_subject_info(subject_number = subject_number)


    pair_num = None
    name_pair = None

    if subject_number % 2 != 0 or round_num != 1:
        pair_num = randint(1,8)
        pair_path = choose_pair(pair_num)
        name_pair = names[randint(0,7)].split(" ")

    else:
        last_subject = retrieve_subject_info(subject_number - 1)
        pair_path = choose_pair(last_subject[3])
        name_pair = [last_subject[5], last_subject[4]]


    window = visual.Window([1680,1050],
                          monitor = "testMonitor",
                          units = "pix",
                          rgb=(-1,-1,-1),
                          fullscr = True)

    subject_image_pair = ImagePair(pair_path, name_pair)
    trial = Trial(window, subject_number, round_num, dom_eye, subject_image_pair,
                  pair_num)

    while True:
        training.main(trial)
        if memory.main(trial):
            break
        else:
            round_num = trial.round_number + 1
            pair_num = randint(1,8)
            pair_path = choose_pair(pair_num)
            name_pair = names[randint(0,7)].split(" ")

            subject_image_pair = ImagePair(pair_path, name_pair)
            trial = Trial(window,subject_number, round_num, dom_eye,
                          subject_image_pair, pair_num)

    end_section(trial.window)
    testing.main(trial)
    end_section(trial.window)
    memory.main(trial, True)
    end_section(trial.window, True)
    window.close()


if __name__ == '__main__':
    main()
