from psychopy import visual, core, event
from psychopy.visual import ImageStim, TextStim
from helpers import retrieve_subject_info, choose_pair, get_user_input
import os, csv


def test_image(window, name, image):
    image.setAutoDraw(True)
    window.flip()
    name = get_user_input(window, (0,-150))
    image.setAutoDraw(False)

    return name


def write_to_csv(new_experiment, subject_number, name_1, remembered_name_1,
                 name_2, remembered_name_2, foil_name_1, foil_name_2):


    data = [subject_number, name_1, remembered_name_1, name_2,
            remembered_name_2, foil_name_1, foil_name_2]

    with open("memory_results.csv", 'ab') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_ALL)

        wr.writerow(data)



def main(window, trial):


    pair_num = trial.pair_num
    img_1 = trial.image_pair.images[0]
    img_2 = trial.image_pair.images[1]
    name_1 = img_1.name
    name_2 = img_2.name

    pic_1 = img_1.stimulus(window, size = 200)
    foil_1 = img_1.foil(window)

    pic_2 = img_2.stimulus(window, size = 200)
    foil_2 = img_2.foil(window)


    remembered_name_1 = test_image(window, name_1, pic_1)
    foil_name_1 = test_image(window, "NA", foil_1)

    remembered_name_2 = test_image(window, name_2, pic_2)
    foil_name_2 = test_image(window, foil_2)

    write_to_csv(subject_number = subject_number,
                 name_1 = name_1,
                 remembered_name_1 = remembered_name_1,
                 name_2 = name_2,
                 remembered_name_2 = remembered_name_2,
                 foil_name_1 = foil_name_1,
                 foil_name_2 = foil_name_2)



if __name__ == '__main__':
    main()
