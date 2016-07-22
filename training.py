from psychopy import visual, core, event
from random import randint
from helpers import choose_pair, get_subject_info
import os
import csv


def show_pair(mywin, path_string, name_1, name_2):
    """
    Shows the pair of images on the screen, with a 2 second delay between images
    """
    #TODO: figure out positioning of elements
    #TODO: figure out name generation

    pair_names = [name_1, name_2]
    for i in range(1,3):
        img_file = path_string + str(i) + ".png"
        name = pair_names[i-1]

        img = visual.ImageStim(mywin, image = img_file, color=(1,1,1),
                               size=[5, 5], pos =(-10,0))
        label = visual.TextStim(mywin, text=name, pos=(10,0),
                                alignHoriz='center', alignVert='center')

        img.draw()
        label.draw()
        mywin.flip()
        core.wait(2)

def write_to_file(new_experiment, subject_number, round_num, dom_eye, pair_num):
    """
    Writes subject and pairs to results.csv
    """
    if new_experiment:
        if(os.path.exists('training_results.csv')):
            os.remove('training_results.csv')
    subject_data = [subject_number, round_num, dom_eye, pair_num]

    file_exists = os.path.exists('training_results.csv')

    with open('training_results.csv', 'ab') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_ALL)

        if new_experiment:
            header = ["Subject Number", "Round Number", "Dominant Eye", "Pair Number"]
            wr.writerow(header)

        wr.writerow(subject_data)

def main(new_experiment = False, names = ['Name 1', 'Name 2'], subject_number = 1):
    #TODO: screensize

    round_num, dom_eye = get_subject_info(training = True,
                                          subject_number = subject_number)

    #create window
    mywin = visual.Window([1920,1080], monitor = "testMonitor",
                          units = "deg", rgb=(-1,-1,-1), fullscr = True)


    pair_num = randint(1,16)

    pair_path = choose_pair(pair_num)
    name_1 = names[0]
    name_2 = names[1]
    show_pair(mywin, pair_path, name_1, name_2)

    mywin.close()

    write_to_file(new_experiment, subject_number, round_num, dom_eye, pair_num)

if __name__ == '__main__':
    main()
