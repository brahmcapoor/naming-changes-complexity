from psychopy import visual, core, event
from psychopy.visual import ImageStim, TextStim, Circle
from random import randint
from helpers import choose_pair, get_subject_info, read_csv
from experiment_objects import ImagePair, Image
import os
import csv


def show_pair_with_names(window, images):
    """
    Shows the pair of images on the screen, with a 2 second delay between images
    """

    stimuli = map(lambda image: image.stimulus(window,
                                               position = (0,0),
                                               size = 400), images)

    labels = map(lambda image: image.label(window,
                                           position = (0, -250)), images)

    for i in range(2):
        image = stimuli[i]
        label = labels[i]

        for frameN in range(300):
            image.draw()
            label.draw()
            window.flip()

def show_both_images(window, images):
    """
    Shows both images in the pair for 10s, without their corresponding names
    """

    img_1 = images[0].stimulus(window, (-200,0), 200)
    img_2 = images[1].stimulus(window, (200,0), 200)

    for frameN in range(600):
        img_1.draw()
        img_2.draw()
        window.flip()


def write_to_file(subject_number, round_num, dom_eye, pair_num, name_1, name_2):
    """
    Writes subject and pairs to results.csv
    """
    subject_data = [subject_number, round_num, dom_eye, pair_num, name_1, name_2]

    with open('training_results.csv', 'ab') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_NONE)
        wr.writerow(subject_data)


def main(window, trial):

    images = trial.image_pair.images
    show_both_images(window, images)
    show_pair_with_names(window, images)

    write_to_file(subject_number = trial.subject_number,
                  round_num = trial.round_number,
                  dom_eye = trial.dominant_eye,
                  pair_num = trial.pair_num,
                  name_1 = images[0].name,
                  name_2 = images[1].name)

if __name__ == '__main__':
    main()
