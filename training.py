from psychopy import visual, core, event
from random import sample
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


def write_to_file(subject_number, pairs, names):
    """
    Writes subject and pairs to results.csv
    """

    subject_data = [subject_number, pairs, names]

    file_exists = os.path.exists('training_results.csv')

    with open('training_results.csv', 'ab') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_ALL)

        if not file_exists:
            header = ["Subject Number", "Pairs", "Names"]
            wr.writerow(header)

        wr.writerow(subject_data)


def generate_names(num_pairs):
    """
    Generates names for the images. Within each pair, there is one easy name
    and one hard name
    """

    #TODO: naming procedure
    #TODO: Distinguish between easy/hard names. Maybe just first is easier?
    for i in range(num_pairs):
        pass
    return ['name 1', 'name 2', 'name 3', 'name 4']


def main():
    #TODO: figure out how many pairs to show
    #TODO: background color
    #TODO: screensize


    subject_num, num_pairs = get_subject_info(training = True)

    #create window
    mywin = visual.Window([1920,1080], monitor = "testMonitor",
                          units = "deg", rgb=(-1,-1,-1), fullscr = True)


    chosen_pairs = sample(range(1,16), num_pairs)
    names = generate_names(num_pairs)

    for index,pair_num in enumerate(chosen_pairs):
        pair_path = choose_pair(pair_num)
        name_1 = names[2 * index]
        name_2 = names[2 * index + 1]
        show_pair(mywin, pair_path, name_1, name_2)
    mywin.close()

    write_to_file(subject_num, chosen_pairs, names)

if __name__ == '__main__':
    main()
