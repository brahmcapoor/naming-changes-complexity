from psychopy import visual, core, event, gui
from random import sample
from helpers import choose_pair
import os
import csv

def show_pair(mywin, path_string):
    """
    Shows the pair of images on the screen, with a 2 second delay between images
    """
    #TODO: figure out positioning of elements
    #TODO: figure out name generation

    for i in range(1,3):
        img_file = path_string + str(i) + ".png"
        name = "Name " + str(i)

        img = visual.ImageStim(mywin, image = img_file, color=(1,1,1),
                               size=[5, 5], pos =(-10,0))
        label = visual.TextStim(mywin, text=name, pos=(10,0),
                                alignHoriz='center', alignVert='center')

        img.draw()
        label.draw()
        mywin.flip()
        core.wait(2)

def write_to_file(subject_number, pairs):
    """
    Writes subject and pairs to results.csv
    """
    #TODO: save names
    subject_data = [subject_number, pairs]
    file_exists = os.path.exists('results.csv')
    with open('results.csv', 'ab') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_ALL)
        if not file_exists:
            header = ["Subject Number", "Pairs", "Names"]
            wr.writerow(header)
        wr.writerow(subject_data)


def main():
    #TODO: figure out how many pairs to show
    #TODO: background color
    #TODO: screensize


    #Ask how many pairs
    input = gui.Dlg(title = "Training")
    input.addField('Subject Number')
    input.addField('Number of pairs')
    input.show()
    num_pairs = int(input.data[1])

    #create window
    mywin = visual.Window([1920,1080], monitor = "testMonitor",
                          units = "deg", rgb=(-1,-1,-1), fullscr = True)
    chosen_pairs = sample(range(1,16), num_pairs)
    for i in chosen_pairs:
        pair_path = choose_pair(i)
        show_pair(mywin, pair_path)
    mywin.close()

    write_to_file(input.data[0], chosen_pairs)

if __name__ == '__main__':
    main()
