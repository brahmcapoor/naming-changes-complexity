from psychopy import visual, core, event
from psychopy.visual import Rect, Circle, ImageStim, TextStim
from psychopy.core import Clock
from random import sample, choice, shuffle
from helpers import choose_pair, retrieve_subject_info, get_subject_info
from copy import deepcopy
import os, csv


def step(window, transparencies, img, frames, i):
    """
    Performs a single 'step' for the staircase method.

    If a key is pressed, the subject has seen the stimulus and has pressed a
    key, meaning the stimulus must be more transparent in the next presentation
    """

    text_1 = TextStim(win = window,
                      text = "Press space if \nyou saw something",
                      pos= (200, 150),
                      alignHoriz = 'center',
                      alignVert = 'center')

    text_2 = TextStim(win = window,
                      text = "Press space if \nyou saw something",
                      pos = (-200,150),
                      alignHoriz = 'center',
                      alignVert = 'center')

    increment = 0.02
    if i > 19:
        increment = 0.01
    pressToContinue(window)

    img.setAutoDraw(True)

    clock = Clock()
    keys = event.getKeys(timeStamped = clock)

    seen = False
    for frameN in range(60):
        opacity = transparencies[frameN]
        img.opacity = opacity
        frame_num = frameN//6
        mask_frame = frames[frame_num]

        mask_frame.draw()

        keys = event.getKeys(['space'], timeStamped = clock)
        if keys:
            seen = True
            break

        window.flip()

    img.setAutoDraw(False)

    # Mask shows for 100ms longer
    for frameN in range(6):
        frame_num = frameN//6
        mask_frame = frames[frame_num]

        mask_frame.draw()

        if not seen:
            keys = event.getKeys(['space'], timeStamped = clock)
            if keys:
                seen = True

        window.flip()

    if not seen:
        for frameN in range(54) :
            text_1.draw()
            text_2.draw()
            keys = event.getKeys(['space'], timeStamped = clock)
            if keys:
                seen = True
                break
            window.flip()

    window.flip()

    if seen:
        if keys[0][1] < 0.2:
            #they probably pressed the space bar by mistake
            return [0, "DISCOUNTED TRIAL"]
        else:
            return [-1*increment, keys[0][1]]
    else:
        return [increment, "NO RESPONSE"]

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

def catch_trial(window, image, frames, visible, dominant_eye):

    text_1 = TextStim(win = window,
                      text = "Press space if \nyou saw something",
                      pos= (200, 150),
                      alignHoriz = 'center',
                      alignVert = 'center')

    text_2 = TextStim(win = window,
                      text = "Press space if \nyou saw something",
                      pos = (-200,150),
                      alignHoriz = 'center',
                      alignVert = 'center')


    if dominant_eye:
        img_pos = 200
    else:
        img_pos = -200

    pressToContinue(window)
    transparency = None
    if visible:
        transparency = 1
    else:
        transparency = 0

    img_1 = image.stimulus(window,
                           position = (img_pos, 150),
                           transparency = 0)


    clock = Clock()

    keys = event.getKeys('space')

    skip_to_end = False

    for frameN in range(64):
        opacity = 0.015625 * frameN*transparency

        img_1.setOpacity(opacity)

        frame_num = (frameN//6)%10

        mask_frame_1 = frames[frame_num]

        mask_frame_1.draw()


        img_1.draw()


        keys = event.getKeys(['space'])
        if keys:
            skip_to_end = True
            break

        window.flip()

    window.flip()

    for frameN in range(6):
        if skip_to_end:
            break
        frame_num =  frameN//10
        mask_frame_1 = frames[frame_num]

        mask_frame_1.draw()

        keys = event.getKeys(['space'])
        if keys:
            skip_to_end = True

        window.flip()

    if not skip_to_end:
        for frameN in range(54) :
            text_1.draw()
            text_2.draw()
            keys = event.getKeys(['space'])
            if keys:
                break
            window.flip()

    window.flip()

    if keys:
        return 1
    else:
        return 0

def staircase(window, images, dominant_eye):
    """
    Performs a single staircase to find the threshold of visibility for a
    subject

    returns the threshold
    """

    if dominant_eye:
        maskPos = 200
    else:
        maskPos = -200
    # Image stuff

    img_1_low_contrast = images[0].stimulus(window,
                                            position = (-1 * maskPos, 150),
                                            transparency = 0.1)

    img_1_high_contrast = images[0].stimulus(window,
                                            position = (-1 * maskPos, 150),
                                            transparency = 0.5)

    img_2_low_contrast = images[1].stimulus(window,
                                position = (-1 * maskPos, 150),
                                transparency = 0.1)

    img_2_high_contrast = images[1].stimulus(window,
                                position = (-1 * maskPos, 150),
                                transparency = 0.5)

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
                                            opacity = 1), frame_paths)

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

    #catch trials
    N_TRIALS = 192
    all_trials = [i for i in range(N_TRIALS)]
    shuffle(all_trials)

    easy_low_contrast = all_trials[:40]
    easy_low_contrast.sort()
    easy_high_contrast = all_trials[40:80]
    easy_high_contrast.sort()

    hard_low_contrast = all_trials[80:120]
    hard_low_contrast.sort()
    hard_high_contrast = all_trials[120:160]
    hard_high_contrast.sort()

    invisible_trials = all_trials[160:176]
    visible_trials = all_trials[176:]

    easy_low_contrast_current = 0.1
    easy_high_contrast_current = 0.5

    hard_low_contrast_current = 0.1
    hard_high_contrast_current = 0.5

    visible_seen = 0
    invisible_seen = 0
    invalid_trials = 0

    transparency_log_1 = []
    transparency_log_2 = []
    transparency_log_3 = []
    transparency_log_4 = []

    response_times_1 = []
    response_times_2 = []
    response_times_3 = []
    response_times_4 = []

    i = 0
    while i < N_TRIALS:

        if i in invisible_trials:
            invisible_seen += catch_trial(window, choice(images), frames, False, dominant_eye)
            i += 1
        elif i in visible_trials:
            visible_seen += catch_trial(window, choice(images), frames, True, dominant_eye)
            i += 1

        elif i in easy_low_contrast:
            transparencies = [0.016 * (n + 1) for n in range(60)]
            transparencies = map(lambda n: n * easy_low_contrast_current, transparencies)
            result = step(window, transparencies, img_1_low_contrast, frames, easy_low_contrast.index(i))
            if result[1] != 'DISCOUNTED TRIAL':
                transparency_log_1.append(easy_low_contrast_current)
                easy_low_contrast_current += result[0]
                response_times_1.append(result[1])
                i += 1
            else:
                invalid_trials += 1
        elif i in easy_high_contrast:
            transparencies = [0.016 * (n + 1) for n in range(60)]
            transparencies = map(lambda n: n * easy_high_contrast_current, transparencies)
            result = step(window, transparencies, img_1_high_contrast, frames, easy_high_contrast.index(i))
            if result[1] != 'DISCOUNTED TRIAL':
                transparency_log_2.append(easy_high_contrast_current)
                easy_high_contrast_current += result[0]
                response_times_2.append(result[1])
                i += 1
            else:
                invalid_trials += 1
        elif i in hard_low_contrast:
            transparencies = [0.016 * (n + 1) for n in range(60)]
            transparencies = map(lambda n: n * hard_low_contrast_current, transparencies)
            result = step(window, transparencies, img_2_low_contrast, frames, hard_low_contrast.index(i))
            if result[1] != 'DISCOUNTED TRIAL':
                transparency_log_3.append(hard_low_contrast_current)
                hard_low_contrast_current += result[0]
                response_times_3.append(result[1])
                i += 1
            else:
                invalid_trials += 1
        elif i in hard_high_contrast:
            transparencies = [0.016 * (n + 1) for n in range(60)]
            transparencies = map(lambda n: n * hard_high_contrast_current, transparencies)
            result = step(window, transparencies, img_2_high_contrast, frames, hard_high_contrast.index(i))
            if result[1] != 'DISCOUNTED TRIAL':
                transparency_log_4.append(hard_high_contrast_current)
                hard_high_contrast_current += result[0]
                response_times_4.append(result[1])
                i += 1
            else:
                invalid_trials += 1


        if easy_low_contrast_current > 1:
            easy_low_contrast_current = 1
        if easy_low_contrast_current < 0:
            easy_low_contrast_current = 0
        if easy_high_contrast_current > 1:
            easy_high_contrast_current = 1
        if easy_high_contrast_current < 0:
            easy_low_contrast_current = 0
        if hard_low_contrast_current > 1:
            hard_low_contrast_current = 1
        if hard_low_contrast_current < 0:
            easy_low_contrast_current = 0
        if hard_high_contrast_current > 1:
            hard_high_contrast_current = 1
        if hard_high_contrast_current < 0:
            hard_high_contrast_current = 0

        img_1_low_contrast.setOpacity(easy_low_contrast_current)
        img_1_high_contrast.setOpacity(easy_high_contrast_current)
        img_2_low_contrast.setOpacity(hard_low_contrast_current)
        img_2_high_contrast.setOpacity(hard_high_contrast_current)


    box_1.setAutoDraw(False)
    box_2.setAutoDraw (False)
    fixation_dot_1.setAutoDraw(False)
    fixation_dot_2.setAutoDraw(False)

    window.flip()

    transparencies = [easy_low_contrast_current,
                      easy_high_contrast_current,
                      hard_low_contrast_current,
                      hard_high_contrast_current]

    transparency_logs = [transparency_log_1,
                         transparency_log_2,
                         transparency_log_3,
                         transparency_log_4]

    response_time_logs = [response_times_1,
                          response_times_2,
                          response_times_3,
                          response_times_4]

    return [transparencies, response_time_logs, transparency_logs, visible_seen,
            invisible_seen, invalid_trials]

def write_to_csv(trial, individual_results, first_average, second_average):

    data = [trial.subject_number, individual_results, first_average, second_average, [image.name for image in trial.image_pair.images]]

    with open('testing_results.csv', 'ab') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        wr.writerow(data)

def create_subject_log(subject_number, response_times, transparency_logs,
                       visible_seen, invisible_seen, invalid_trials):

    filename = "subject logs/subject {}.csv".format(subject_number)

    with open(filename, 'wb') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)

        header = ["Trial number", "Transparency", "Response time", "Transparency", "Response time", "Transparency", "Response time", "Transparency", "Response time"]
        wr.writerow(header)

        for i in range(len(response_times[1])):
            row = [i+1, transparency_logs[0][i], response_times[0][i],
                   transparency_logs[1][i], response_times[1][i],
                   transparency_logs[2][i], response_times[2][i],
                   transparency_logs[3][i], response_times[3][i]]
            wr.writerow(row)

    with open('subject logs/catch trials.csv', 'ab') as f:
        wr = csv.writer(f, quoting = csv.QUOTE_NONNUMERIC)

        data = [subject_number, visible_seen, invisible_seen, invalid_trials]

        wr.writerow(data)

def main(trial):

    window = trial.window

    dominant_eye = trial.dominant_eye
    pair_num = trial.pair_num

    images = trial.image_pair.images

    results = staircase(window, images, dominant_eye)

    result_10, result_11, result_20, result_21 = tuple(results[0])

    response_times = results[1]

    transparency_logs = results[2]

    visible_seen = results[3]
    invisible_seen = results[4]
    invalid_trials = results[5]

    create_subject_log(trial.subject_number, response_times, transparency_logs,
                       visible_seen, invisible_seen, invalid_trials)

    img_1_avg = (result_10 + result_11)/2
    img_2_avg = (result_20 + result_21)/2

    individual_results = [result_10, result_11, result_20, result_21]

    write_to_csv(trial, individual_results, img_1_avg, img_2_avg)


if __name__ == "__main__":
    main()
