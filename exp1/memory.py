from psychopy import visual, core, event
from psychopy.visual import ImageStim, TextStim
from random import sample
import os
import csv

"""
I'M NOT GOING TO COMMENT THIS THROUGHOUT, SO THIS IS HOW ANIMATION WORKS:

for frameN in range(number_of_seconds * monitory_refresh_rate):
    do_some_stuff()
    window.flip()

window.flip() refreshes the monitor

(Timing is only precise on a computer with a graphics card)
"""


def get_user_input(window, position, fontsize=50):

    """
    Allows the user to type and see what they type on the screen

    (This is more annoying than it should be on Psychopy, but it works fine now
    so you shouldn't need to change it)
    """

    input_name = ""
    user_input = TextStim(win=window,
                          text=input_name,
                          pos=position,
                          height=fontsize)

    user_input.setAutoDraw(True)
    window.flip()

    while True:
        char = event.waitKeys()[0]
        if char.isalpha() and len(char) == 1:
            input_name += char
        if char == 'return':
            user_input.setAutoDraw(False)
            window.flip()
            return input_name
        if char == 'comma':
            # psychopy inexplicably doesn't respond to the backspace key,
            # so I use the '<' symbol instead
            input_name = input_name[:-1]

        user_input.text = input_name
        window.flip()


def feedback(correct, window):

    """
    Shows feedback (Correct! or Wrong!) after each test
    """
    feedback_text = None
    color = None

    if correct:
        feedback_text = "Correct!"
        color = "Green"
    else:
        feedback_text = "Wrong"
        color = "Red"

    feedback = TextStim(win=window,
                        text=feedback_text,
                        pos=(0, 0),
                        alignHoriz='center',
                        alignVert='center',
                        height=50,
                        color=color)

    feedback.setAutoDraw(True)

    for frameN in range(60):
        window.flip()

    feedback.setAutoDraw(False)

    window.flip()


def test_image(window, name, image):
    """
    Tests a single input
    """
    image.setAutoDraw(True)
    window.flip()
    typed_name = get_user_input(window, (0, -150))
    image.setAutoDraw(False)
    window.flip()

    feedback(typed_name == name, window)

    return typed_name


def write_to_csv(subject_number, round_number, name_1, remembered_name_1,
                 name_2, remembered_name_2, foil_name_1, foil_name_2,
                 final):

    """
    Writes data to csv
    """

    data = [subject_number, round_number, name_1, remembered_name_1, name_2,
            remembered_name_2, foil_name_1, foil_name_2]

    if not final:
        filename = "memory_results_before.csv"
    else:
        filename = "memory_results_after.csv"

    with open(filename, 'ab') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC, lineterminator='\n')

        wr.writerow(data)


def main(trial, final=False):

    """
    The final parameter is to differentiate between the names at the start and
    the end.
    """

    window = trial.window

    pair_num = trial.pair_num
    round_number = trial.round_number
    img_1 = trial.image_pair.images[0]
    img_2 = trial.image_pair.images[1]
    name_1 = img_1.name
    name_2 = img_2.name

    pic_1 = img_1.stimulus(window, size=200)
    foil_1 = img_1.foil(window)

    pic_2 = img_2.stimulus(window, size=200)
    foil_2 = img_2.foil(window)

    remembered_name_1 = (window, name_1, pic_1)
    foil_name_1 = (window, "", foil_1)
    remembered_name_2 = (window, name_2, pic_2)
    foil_name_2 = (window, "", foil_2)

    subject_inputs = [remembered_name_1, foil_name_1, remembered_name_2,
                      foil_name_2]

    for index in sample([0, 1, 2, 3], 4):
        subject_inputs[index] = test_image(*subject_inputs[index])

    remembered_name_1, foil_name_1, remembered_name_2, foil_name_2 = \
        tuple(subject_inputs)

    write_to_csv(subject_number=trial.subject_number,
                 round_number=round_number,
                 name_1=name_1,
                 remembered_name_1=remembered_name_1,
                 name_2=name_2,
                 remembered_name_2=remembered_name_2,
                 foil_name_1=foil_name_1,
                 foil_name_2=foil_name_2,
                 final=final)

    all_correct = remembered_name_1 == name_1 and remembered_name_2 == name_2 \
        and foil_name_1 == "" and foil_name_2 == ""

    return all_correct

if __name__ == '__main__':
    main()
