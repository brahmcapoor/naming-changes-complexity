from psychopy import visual, core, event
from psychopy.visual import Rect, Circle, ImageStim, TextStim
from psychopy.core import Clock
from random import sample
from helpers import choose_pair, retrieve_subject_info, get_subject_info
import os, csv


def step(window, transparencies, img, frames):
    """
    Performs a single 'step' for the staircase method.

    If a key is pressed, the subject has seen the stimulus and has pressed a
    key, meaning the stimulus must be more transparent in the next presentation
    """

    pressToContinue(window)

    img.setAutoDraw(True)

    for frameN in range(60):
        transparency = transparencies[frameN]
        img.opacity = transparency
        frame_num = frameN//6
        mask_frame = frames[frame_num]

        mask_frame.draw()
        window.flip()

    img.setAutoDraw(False)

    # Mask shows for 100ms longer
    for frameN in range(6):
        frame_num = frameN//6
        mask_frame = frames[frame_num]

        mask_frame.draw()
        window.flip()

    window.flip()

    clock = Clock()
    keys = event.waitKeys(maxWait = 1, timeStamped = clock)

    img.setAutoDraw(False)
    if keys and keys[0][0] == 'space':
        return [-0.02, keys[0][1], transparency]
    else:
        return [0.02, "NO RESPONSE", transparency]

def pressToContinue(window):
    """
    Implements "Press to continue" between trials
    """

    text_1 = TextStim(win = window,
                      text = "Press space to \ncontinue",
                      pos= (200, 150),
                      alignHoriz = 'center',
                      alignVert = 'center')

    text_2 = TextStim(win = window,
                      text = "Press space to \ncontinue",
                      pos = (-200,150),
                      alignHoriz = 'center',
                      alignVert = 'center')

    text_1.draw()
    text_2.draw()

    window.flip()
    event.waitKeys()
    window.flip()

def staircase(window, image, transparency, dominant_eye):
    """
    Performs a single staircase to find the threshold of visibility for a
    subject

    returns the threshold
    """

    if dominant_eye == "True":
        maskPos = 200
    else:
        maskPos = -200
    # Image stuff

    img = image.stimulus(window,
                         position = (-1 * maskPos, 150),
                         transparency = transparency)

    # Fusion box stuff

    box_1 = Rect(win = window,
                 width = 180,
                 height = 180,
                 lineWidth = 4,
                 lineColor = 'grey',
                 pos = (maskPos, 150),
                 autoDraw = True)

    box_2 = Rect(win = window,
                 width = 180,
                 height = 180,
                 lineWidth = 4,
                 lineColor = 'grey',
                 pos = (-1 * maskPos, 150),
                 autoDraw = True)

    box_1.setAutoDraw(True)
    box_2.setAutoDraw(True)

    # Mask stuff

    frame_paths = ["Masks/" + file for file in os.listdir("Masks")]
    frames = map(lambda file_name: ImageStim(window,
                                            image = file_name,
                                            color = (1,1,1),
                                            size = [150, 150],
                                            pos = (maskPos,150),
                                            opacity = 0.2), frame_paths)

    #Fixation dot stuff

    fixation_dot_1 = Circle(win = window,
                          radius = 2,
                          fillColor = 'red',
                          pos = (maskPos, 150),
                          lineWidth = 0,
                          autoDraw = True)

    fixation_dot_2 = Circle(win = window,
                          radius = 2,
                          fillColor = 'red',
                          pos = (-1 * maskPos, 150),
                          lineWidth = 0,
                          autoDraw = True)


    response_times = []
    transparency_log = []

    for i in range(40):
        transparencies = [0.016 * (n + 1) for n in range(60)]
        transparencies = map(lambda n: n * transparency, transparencies)
        result = step(window, transparencies, img, frames)
        transparency += result[0]
        response_times.append(result[1])
        transparency_log.append(result[2])

        if transparency > 1:
            transparency = 1
        if transparency < 0:
            transparency = 0

    box_1.setAutoDraw(False)
    box_2.setAutoDraw (False)
    fixation_dot_1.setAutoDraw(False)
    fixation_dot_2.setAutoDraw(False)

    window.flip()

    return [transparency, response_times, transparency_log]

def write_to_csv(trial, individual_results, first_average, second_average):

    data = [trial.subject_number, individual_results, first_average, second_average, [image.name for image in trial.image_pair.images]]

    with open('testing_results.csv', 'ab') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        wr.writerow(data)

def create_subject_log(subject_number, response_times, transparency_logs):

    filename = "subject logs/subject {}.csv".format(subject_number)

    with open(filename, 'wb') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)

        header = ["Trial number, ""Transparency", "Response time", "Transparency", "Response time", "Transparency", "Response time", "Transparency", "Response time"]
        wr.writerow(header)

        for i in range(len(response_times[1])):
            row = [i, transparency_logs[0][i], response_times[0][i],
                   transparency_logs[1][i], response_times[1][i],
                   transparency_logs[2][i], response_times[2][i],
                   transparency_logs[3][i], response_times[3][i]]
            wr.writerow(row)


def main(trial):

    window = trial.window

    dominant_eye = trial.dominant_eye
    pair_num = trial.pair_num

    images = trial.image_pair.images

    img_1 = images[0]
    img_2 = images[1]

    result_10 = (window, img_1, 0, dominant_eye)
    result_11 = (window, img_1, 1, dominant_eye)
    result_20 = (window, img_2, 0, dominant_eye)
    result_21 = (window, img_2, 1, dominant_eye)

    results = [result_10, result_11, result_20, result_21]

    for index in sample([0,1,2,3], 4):
        results[index] = staircase(*results[index])

    result_10, result_11, result_20, result_21 = tuple(result[0] for result in results)

    response_times = [result[1] for result in results]
    transparency_logs = [result[2] for result in results]

    create_subject_log(trial.subject_number, response_times, transparency_logs)

    img_1_avg = (result_10 + result_11)/2
    img_2_avg = (result_20 + result_21)/2

    individual_results = [result_10, result_11, result_20, result_21]

    write_to_csv(trial, individual_results, img_1_avg, img_2_avg)

if __name__ == "__main__":
    main()
