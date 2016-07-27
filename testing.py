from psychopy import visual, core, event
from random import sample
from helpers import choose_pair, retrieve_subject_info, get_subject_info
import os, csv


def step(window, transparency, img, frames):
    """
    Performs a single 'step' for the staircase method.

    If a key is pressed, the subject has seen the stimulus and has pressed a
    key, meaning the stimulus must be more transparent in the next presentation
    """
    #TODO: How much longer should mask be shown?

    img.setOpacity(transparency)
    img.setAutoDraw(True)

    for frameN in range(60):

        frame_num = frameN//6
        mask_frame = frames[frame_num]


        mask_frame.draw()
        window.flip()

    img.setAutoDraw(False)
    window.flip()

    keys = event.waitKeys(maxWait = 2)

    if keys:
        return -0.02
    else:
        return 0.02



def staircase(window, image, transparency, dominant_eye):
    """
    Performs a single staircase to find the threshold of visibility for a
    subject

    returns the threshold
    """

    if dominant_eye == "True":
        maskPos = 125
    else:
        maskPos = -125
    # Image stuff
    img = visual.ImageStim(window,
                           image = image,
                           color=(1,1,1),
                           size = [145,145],
                           pos = (-1 * maskPos,0),
                           opacity = transparency)


    # Mask stuff
    frame_paths = ["Masks/" + file for file in os.listdir("Masks")]
    frames = map(lambda file_name: visual.ImageStim(window,
                                                    image = file_name,
                                                    color = (1,1,1),
                                                    size = [150, 150],
                                                    pos = (maskPos,0)), frame_paths)

    for i in range(40):
        transparency += step(window, transparency, img, frames)
        if transparency > 1:
            transparency = 1
        if transparency < 0:
            transparency = 0
    return transparency

def write_to_csv(new_experiment, subject_number, difficulties, individual_results, first_average, second_average):

    if new_experiment:
        if(os.path.exists('testing_results.csv')):
            os.remove('testing_results.csv')

    data = [subject_number, difficulties, individual_results, first_average, second_average]

    with open('testing_results.csv', 'ab') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_ALL)

        if new_experiment:
            header = ["Subject Number", "Difficulties", "Individual results", "Image 1 Average", "Image 2 Average"]
            wr.writerow(header)

        wr.writerow(data)


def main(new_experiment =  True, subject_number = 1):

    mywin = visual.Window([1920,1080],
                          monitor = "testMonitor",
                          units = "pix",
                          rgb=(-1,-1,-1),
                          fullscr = True)

    subject_info = retrieve_subject_info(subject_number)
    dominant_eye = subject_info[2]
    pair_num = subject_info[3]
    difficulties = (subject_info[6], subject_info[7])

    pair_path = choose_pair(pair_num)
    img_1 = pair_path + "1.png"
    img_2 = pair_path + "2.png"

    result_10 = staircase(mywin, img_1, 0, dominant_eye)
    result_11 = staircase(mywin, img_1, 1, dominant_eye)
    result_20 = staircase(mywin, img_2, 0, dominant_eye)
    result_21 = staircase(mywin, img_2, 1, dominant_eye)

    img_1_avg = (result_10 + result_11)/2
    img_2_avg = (result_20 + result_21)/2

    individual_results = [result_10, result_11, result_20, result_21]

    write_to_csv(new_experiment, subject_number, difficulties, individual_results, img_1_avg, img_2_avg)

if __name__ == "__main__":
    main()
