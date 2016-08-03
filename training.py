from psychopy import visual, core, event
from psychopy.visual import ImageStim, TextStim, Circle
from random import randint
from helpers import choose_pair, get_subject_info, read_csv
import os
import csv


def show_pair_with_names(window, path_string, name_1, name_2):
    """
    Shows the pair of images on the screen, with a 2 second delay between images
    """

    pair_names = [name_1, name_2]
    for i in range(1,3):
        img_file = path_string + str(i) + ".png"
        name = pair_names[i-1]

        img_1 = ImageStim(window,
                          image = img_file,
                          color=(1,1,1),
                          size=[400, 400],
                          pos =(0,0))

        label_1 = TextStim(window,
                           text=name,
                           pos= (0,-250),
                           alignHoriz='center',
                           alignVert='center',
                           height = 50)

        img_1.setAutoDraw(True)
        label_1.setAutoDraw(True)

        for frameN in range(600):
            window.flip()
        else:
            img_1.setAutoDraw(False)
            label_1.setAutoDraw(False)

def show_both_images(window, path_string):
    """
    Shows both images in the pair for 10s, without their corresponding names
    """

    img_1_path = path_string + "1.png"
    img_2_path = path_string + "2.png"


    pass

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


def main(window, new_experiment = True,
                names = ['Name 1', 'Name 2'],
                subject_number = 1,
                round_num = 1,
                dom_eye = True):


    chosen_pairs = get_chosen_pairs()

    if subject_number % 2 != 0 or round_num != 1:
        #Choose a new pair
        while True:
            pair_num = randint(1,8)
            if str(pair_num) not in chosen_pairs:
                break
        pair_path = choose_pair(pair_num)
        name_pair = names[pair_num]
        name_1, name_2 = tuple(name_pair.split(" "))
        show_pair(window, pair_path, name_1, name_2)
        difficulty_1 = "Easy"
        difficulty_2 = "Difficult"

    else:
        #show the same pair as last time, but with swapped names

        pair_num = chosen_pairs[len(chosen_pairs) -  1]
        pair_path = choose_pair(pair_num)
        name_pair = names[int(pair_num)]
        name_2, name_1 = tuple(name_pair.split(" "))
        show_pair_with_names(window, pair_path, name_1, name_2)
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
