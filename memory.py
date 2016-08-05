from psychopy import visual, core, event
from psychopy.visual import ImageStim, TextStim
from helpers import retrieve_subject_info, choose_pair, get_user_input
from random import sample
import os, csv


def feedback(correct, window):

    feedback_text = None
    color = None

    if correct:
        feedback_text = "Correct!"
        color = "Green"
    else:
        feedback_text = "Wrong"
        color = "Red"

    feedback = TextStim(win = window,
                        text = feedback_text,
                        pos = (0,0),
                        alignHoriz = 'center',
                        alignVert = 'center',
                        height = 50,
                        color = color)

    feedback.setAutoDraw(True)

    for frameN in range(60):
        window.flip()

    feedback.setAutoDraw(False)

    window.flip()


def test_image(window, name, image):
    image.setAutoDraw(True)
    window.flip()
    typed_name = get_user_input(window, (0,-150))
    image.setAutoDraw(False)
    window.flip()

    feedback(typed_name == name, window)

    return typed_name


def write_to_csv(subject_number, round_number, name_1, remembered_name_1,
                 name_2, remembered_name_2, foil_name_1, foil_name_2,
                 final):


    data = [subject_number, round_number, name_1, remembered_name_1, name_2,
            remembered_name_2, foil_name_1, foil_name_2]

    if not final:
        filename = "memory_results_before.csv"
    else:
        filename = "memory_results_after.csv"

    with open(filename, 'ab') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_ALL)

        wr.writerow(data)


def main(window, trial, final = False):

    pair_num = trial.pair_num
    round_number = trial.round_number
    img_1 = trial.image_pair.images[0]
    img_2 = trial.image_pair.images[1]
    name_1 = img_1.name
    name_2 = img_2.name

    pic_1 = img_1.stimulus(window, size = 200)
    foil_1 = img_1.foil(window)

    pic_2 = img_2.stimulus(window, size = 200)
    foil_2 = img_2.foil(window)


    remembered_name_1 = (window, name_1, pic_1)
    foil_name_1 = (window, "", foil_1)
    remembered_name_2 = (window, name_2, pic_2)
    foil_name_2 = (window, "", foil_2)

    subject_inputs = [remembered_name_1, foil_name_1, remembered_name_2, foil_name_2]

    for index in sample([0,1,2,3], 4):
        subject_inputs[index] = test_image(*subject_inputs[index])

    remembered_name_1, foil_name_1, remembered_name_2, foil_name_2 = tuple(subject_inputs)

    write_to_csv(subject_number = trial.subject_number,
                 round_number = round_number,
                 name_1 = name_1,
                 remembered_name_1 = remembered_name_1,
                 name_2 = name_2,
                 remembered_name_2 = remembered_name_2,
                 foil_name_1 = foil_name_1,
                 foil_name_2 = foil_name_2,
                 final = final)

    all_correct = remembered_name_1 == name_1 and remembered_name_2 == name_2   and foil_name_1 == "" and foil_name_2 == ""

    return all_correct

if __name__ == '__main__':
    main()
