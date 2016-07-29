from psychopy import visual, core, event
from psychopy.visual import ImageStim, TextStim, Circle
from random import randint
from helpers import choose_pair, get_subject_info, read_csv
import os
import csv


def show_pair(mywin, path_string, name_1, name_2):
    """
    Shows the pair of images on the screen, with a 2 second delay between images
    """

    pair_names = [name_1, name_2]
    for i in range(1,3):
        img_file = path_string + str(i) + ".png"
        name = pair_names[i-1]

        img_1 = ImageStim(mywin,
                          image = img_file,
                          color=(1,1,1),
                          size=[160, 160],
                          pos =(-200,160))

        label_1 = TextStim(mywin,
                           text=name,
                           pos=(-200,70),
                           alignHoriz='center',
                           alignVert='center')

        img_2 = ImageStim(mywin,
                          image = img_file,
                          color=(1,1,1),
                          size=[160, 160],
                          pos =(200,160))

        label_2 = TextStim(mywin,
                           text=name,
                           pos=(200,70),
                           alignHoriz='center',
                           alignVert='center')

        fixation_dot_1 = Circle(win = mywin,
                                radius = 2,
                                fillColor = 'red',
                                pos = (-200, 160),
                                lineWidth = 0)

        fixation_dot_2 = Circle(win = mywin,
                                radius = 2,
                                fillColor = 'red',
                                pos = (200, 160),
                                lineWidth = 0)

        for frameN in range(120):
            img_1.draw()
            label_1.draw()
            img_2.draw()
            label_2.draw()
            fixation_dot_1.draw()
            fixation_dot_2.draw()
            mywin.flip()
        else:
            return

def write_to_file(new_experiment, subject_number, round_num, dom_eye, pair_num, name_1, name_2,
                  difficulty_1, difficulty_2):
    """
    Writes subject and pairs to results.csv
    """
    if new_experiment:
        if(os.path.exists('training_results.csv')):
            os.remove('training_results.csv')
    subject_data = [subject_number, round_num, dom_eye, pair_num, name_1, name_2,
                    difficulty_1, difficulty_2]

    with open('training_results.csv', 'ab') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_ALL)

        if new_experiment:
            header = ["Subject Number", "Round Number", "Dominant Eye",
                      "Pair Number", "Name 1", "Name 2", "Difficulty 1",
                      "Difficulty 2"]
            wr.writerow(header)

        wr.writerow(subject_data)


def get_chosen_pairs():
    """
    Returns all the pair numbers that have already been chosen
    """
    data = read_csv('training_results.csv')
    return [subject[3] for subject in data]

def main(mywin, new_experiment = True,
                names = ['Name 1', 'Name 2'],
                subject_number = 1,
                round_num = 1,
                dom_eye = True):
    #TODO: screensize


    chosen_pairs = get_chosen_pairs()

    if subject_number % 2 != 0 or round_num != 1:
        #Choose a new pair
        while True:
            pair_num = randint(1,16)
            if str(pair_num) not in chosen_pairs:
                break
        pair_path = choose_pair(pair_num)
        name_pair = names[pair_num]
        name_1, name_2 = tuple(name_pair.split(" "))
        show_pair(mywin, pair_path, name_1, name_2)
        difficulty_1 = "Easy"
        difficulty_2 = "Difficult"

    else:
        #show the same pair as last time, but with swapped names

        pair_num = chosen_pairs[len(chosen_pairs) -  1]
        pair_path = choose_pair(pair_num)
        name_pair = names[int(pair_num)]
        name_2, name_1 = tuple(name_pair.split(" "))
        show_pair(mywin, pair_path, name_1, name_2)
        difficulty_1 = "Difficult"
        difficulty_2 = "Easy"


    write_to_file(new_experiment = new_experiment,
                  subject_number = subject_number,
                  round_num = round_num,
                  dom_eye = dom_eye,
                  pair_num = pair_num,
                  name_1 = name_1,
                  name_2 = name_2,
                  difficulty_1 = difficulty_1,
                  difficulty_2 = difficulty_2)

if __name__ == '__main__':
    main()
