from psychopy import visual, core, event
from psychopy.visual import Rect, Circle, ImageStim, TextStim
from psychopy.core import Clock
from random import sample, choice, shuffle
from copy import deepcopy
import os
import csv

"""
I'M NOT GOING TO COMMENT THIS THROUGHOUT, SO THIS IS HOW ANIMATION & STIMULUS
PRESENTATION WORKS:

for frameN in range(number_of_seconds * monitory_refresh_rate):
    draw_some_stuff()
    window.flip()

window.flip() refreshes the monitor

(Timing is only precise on a computer with a graphics card)


OTHER NOTES:
    This is a very long, relatively intricate at at frequently horrendously
    inelegant implementation, but making incremental changes actually isn't too
    challenging. Just make sure at all times the functions are passing the
    right information to each other.
"""

from psychopy import logging
logging.console.setLevel(logging.WARNING)


def step(window, transparencies, img, frames, i):
    """
    Performs a single 'step' for the staircase method.

    If a key is pressed, the subject has seen the stimulus and has pressed a
    key, meaning the stimulus must be more transparent in the next presentation

    There's a bunch of parameters here:
        window is the psychopy window
        transparencies is a list of transparencies - one per frame - to allow
                        for the ramping up of the image
        img is the stimulus
        frames is an array of all the mask frames
        i is the step number with the staircase, needed to determine the
            increment

    This function returns an increment - positive, negative or 0 if an invalid
    trial - that is added to the transparency on the next step of the staircase
    as well as a timestamp of the keypress or a status as to whether the trial
    was discounted or had no response
    """

    # If a stimulus seems to be duplicated, it is so it can be shown in both
    # eyes

    text_1 = TextStim(win=window,
                      text="Press space if \nyou saw something",
                      pos=(200, 150),
                      alignHoriz='center',
                      alignVert='center')

    text_2 = TextStim(win=window,
                      text="Press space if \nyou saw something",
                      pos=(-200, 150),
                      alignHoriz='center',
                      alignVert='center')

    increment = 0.02

    # changes the increment after half the trials are done.
    if i > 39:
        increment = 0.01
    pressToContinue(window)

    img.setAutoDraw(True)

    # for timing
    clock = Clock()
    keys = event.getKeys(timeStamped=clock)

    # seen becomes True when the space bar key is pressed, indicating
    # that something is seen and so skipping to the end of the trial
    seen = False

    # shows the image and the mask for 1 second.
    for frameN in range(60):
        opacity = transparencies[frameN]
        img.opacity = opacity
        frame_num = frameN//6
        mask_frame = frames[frame_num]

        mask_frame.draw()

        keys = event.getKeys(['space'], timeStamped=clock)
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
            keys = event.getKeys(['space'], timeStamped=clock)
            if keys:
                seen = True

        window.flip()

    # 900 ms more
    if not seen:
        for frameN in range(54):
            text_1.draw()
            text_2.draw()
            keys = event.getKeys(['space'], timeStamped=clock)
            if keys:
                seen = True
                break
            window.flip()

    window.flip()

    if seen:
        if keys[0][1] < 0.2 or transparencies[3] == 0:
            # The second of those two conditions indicates whether the
            # transparency of the image is 0

            # they probably pressed the space bar by mistake
            logging.warn("INVALID TRIAL")  # add this information the log
            return [0, "DISCOUNTED TRIAL"]

        else:
            # They saw it! A valid trial
            logging.warn("SEEN")  # add this information to the log
            return [-1*increment, keys[0][1]]
    else:
        logging.warn("NOT SEEN")
        return [increment, "NO RESPONSE"]


def pressToContinue(window):
    """
    Implements "Press to continue" between trials
    """

    text_1 = TextStim(win=window,
                      text="Press right to \ncontinue",
                      pos=(200, 150),
                      alignHoriz='center',
                      alignVert='center')

    text_2 = TextStim(win=window,
                      text="Press right to \ncontinue",
                      pos=(-200, 150),
                      alignHoriz='center',
                      alignVert='center')

    text_1.draw()
    text_2.draw()

    window.flip()
    while True:
        if event.getKeys(['right']):
            break
    window.flip()


def catch_trial(window, image, frames, visible, dominant_eye):
    """
    Implements catch trials. This works in largely the same way as
    the step function, so only the unique parts of this function are commented.

    The 'visible' parameter is a boolean indicating - surprisingly enough -
    whether it is a visible catch trial.

    This method simply returns 1 or 0, depending on whether something was seen
    and this is added to the count for that respective type of catch trial.
    """
    text_1 = TextStim(win=window,
                      text="Press space if \nyou saw something",
                      pos=(200, 150),
                      alignHoriz='center',
                      alignVert='center')

    text_2 = TextStim(win=window,
                      text="Press space if \nyou saw something",
                      pos=(-200, 150),
                      alignHoriz='center',
                      alignVert='center')

    if dominant_eye:
        img_pos = 200
    else:
        img_pos = -200

    pressToContinue(window)

    transparency = None

    if visible:
        transparency = 0.1
    else:
        transparency = 0

    img_1 = image.stimulus(window,
                           position=(img_pos, 150),
                           transparency=0)

    clock = Clock()

    keys = event.getKeys('space')

    skip_to_end = False

    for frameN in range(64):
        opacity = 0.015625 * frameN*transparency

        img_1.setOpacity(opacity)

        frame_num = (frameN//6) % 10

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
        frame_num = frameN//10
        mask_frame_1 = frames[frame_num]

        mask_frame_1.draw()

        keys = event.getKeys(['space'])
        if keys:
            skip_to_end = True

        window.flip()

    if not skip_to_end:
        for frameN in range(54):
            text_1.draw()
            text_2.draw()
            keys = event.getKeys(['space'])
            if keys:
                break
            window.flip()

    window.flip()

    if keys:
        logging.warn("SEEN")
        return 1
    else:
        logging.warn("NOT SEEN")
        return 0


def staircase(window, images, dominant_eye):
    """
    This is the killer function! It handles all 4 staircases, as well as
    the recording of the subject logs. While it is a pain to go through,
    it's unlikely you'll need to change it much, other than maybe a few
    constants.

    This also ties together all of the other staircase/catch trial functions.
    What this means is that if you want to make a change to the experimental
    PROCEDURE, you'll most likely want to make a change to one of those
    functions.

    If - and this is probably unlikely - you need to change the way the
    experiment handles the data recording and actually INTERACTS with the data
    that each step provides, this is the function you need to jump into...

    The parameters are fairly simple. Images. is the pair of images for the
    subject and dominant_eye is a boolean indicating if the right eye is the
    dominant eye, for positioning purposes.
    """

    # Position of image and mask change based on whether the right eye is
    # dominant

    if dominant_eye:
        maskPos = 200
    else:
        maskPos = -200

    # Image stuff - just converting the images to a format Psychopy can present

    img_1_low_contrast = images[0].stimulus(window,
                                            position=(-1 * maskPos, 150),
                                            transparency=0.1)

    img_1_high_contrast = images[0].stimulus(window,
                                             position=(-1 * maskPos, 150),
                                             transparency=0.5)

    img_2_low_contrast = images[1].stimulus(window,
                                            position=(-1 * maskPos, 150),
                                            transparency=0.1)

    img_2_high_contrast = images[1].stimulus(window,
                                             position=(-1 * maskPos, 150),
                                             transparency=0.5)

    # Fusion box stuff - creating the fusion boxes

    box_1 = Rect(win=window,
                 width=180,
                 height=180,
                 lineWidth=4,
                 lineColor='grey',
                 pos=(maskPos, 150),
                 autoDraw=True)

    box_2 = Rect(win=window,
                 width=180,
                 height=180,
                 lineWidth=4,
                 lineColor='grey',
                 pos=(-1 * maskPos, 150),
                 autoDraw=True)

    box_1.setAutoDraw(True)
    box_2.setAutoDraw(True)

    # Mask stuff - generate the masks

    frame_paths = ["../Masks/" + file for file in os.listdir("Masks")]
    frames = map(lambda file_name: ImageStim(window,
                                             image=file_name,
                                             color=(1, 1, 1),
                                             size=[150, 150],
                                             pos=(maskPos, 150),
                                             opacity=1), frame_paths)

    # Fixation dot stuff

    fixation_dot_1 = Circle(win=window,
                            radius=2,
                            fillColor='red',
                            pos=(maskPos, 150),
                            lineWidth=0,
                            autoDraw=True)

    fixation_dot_2 = Circle(win=window,
                            radius=2,
                            fillColor='red',
                            pos=(-1 * maskPos, 150),
                            lineWidth=0,
                            autoDraw= True)

    response_times = []
    transparency_log = []

    # figuring out which trials fall into which staircase.

    N_TRIALS = 384
    all_trials = [i for i in range(N_TRIALS)]  # stores an array of all trials
    shuffle(all_trials)  # randomizes

    # now we separate the list into smaller lists of trial numbers and sort
    # those lists in ascending order. We sort them so that we know within
    # each list, what the first 20 and what the last 20 trials are so
    # that we can change the increment

    easy_low_contrast = all_trials[:80]
    easy_low_contrast.sort()
    easy_high_contrast = all_trials[80:160]
    easy_high_contrast.sort()

    hard_low_contrast = all_trials[160:240]
    hard_low_contrast.sort()
    hard_high_contrast = all_trials[240:320]
    hard_high_contrast.sort()

    invisible_trials = all_trials[320:352]
    visible_trials = all_trials[352:]

    # the four staircase values currently
    easy_low_contrast_current = 0.1
    easy_high_contrast_current = 0.5

    hard_low_contrast_current = 0.1
    hard_high_contrast_current = 0.5

    # to be recorded to check if subject is valid
    visible_seen = 0
    invisible_seen = 0
    invalid_trials = 0

    # the list of the transparencies for each staircase
    transparency_log_1 = []
    transparency_log_2 = []
    transparency_log_3 = []
    transparency_log_4 = []

    # the list of response times for each staircase
    response_times_1 = []
    response_times_2 = []
    response_times_3 = []
    response_times_4 = []

    i = 0
    while i < N_TRIALS:
        # i increases only when a valid trial occurs. Otherwise, it doesn't
        # increase and the trial is repeated.

        logging.warn("TRIAL " + str(i) + ":")

        if i in invisible_trials:
            logging.warn("INVISIBLE CATCH TRIAL")
            invisible_seen += catch_trial(window, choice(images),
                                          frames, False, dominant_eye)
            i += 1
        elif i in visible_trials:
            logging.warn("VISIBLE CATCH TRIAL")
            visible_seen += catch_trial(window, choice(images),
                                        frames, True, dominant_eye)
            i += 1

        elif i in easy_low_contrast:
            logging.warn("EASY LOW CONTRAST")
            transparencies = [0.016 * (n + 1) for n in range(60)]
            transparencies = map(lambda n: n * easy_low_contrast_current,
                                 transparencies)
            # this array is a list of the transparencies required for the image
            # to ramp up

            result = step(window, transparencies, img_1_low_contrast, frames,
                          easy_low_contrast.index(i))

            if result[1] != 'DISCOUNTED TRIAL':  # checks if trial is valid
                transparency_log_1.append(easy_low_contrast_current)
                easy_low_contrast_current += result[0]
                # change the transparency for this staircase
                response_times_1.append(result[1])
                i += 1
            else:
                # invalid trial
                invalid_trials += 1

        # ALL OTHER TRIALS FOLLOW THE SAME PATTERN AS ABOVE

        elif i in easy_high_contrast:
            logging.warn("EASY HIGH CONTRAST")
            transparencies = [0.016 * (n + 1) for n in range(60)]
            transparencies = map(lambda n: n * easy_high_contrast_current,
                                 transparencies)
            result = step(window, transparencies, img_1_high_contrast, frames,
                          easy_high_contrast.index(i))
            if result[1] != 'DISCOUNTED TRIAL':
                transparency_log_2.append(easy_high_contrast_current)
                easy_high_contrast_current += result[0]
                response_times_2.append(result[1])
                i += 1
            else:
                invalid_trials += 1

        elif i in hard_low_contrast:
            logging.warn("HARD LOW CONTRAST")
            transparencies = [0.016 * (n + 1) for n in range(60)]
            transparencies = map(lambda n: n * hard_low_contrast_current,
                                 transparencies)
            result = step(window, transparencies, img_2_low_contrast, frames,
                          hard_low_contrast.index(i))
            if result[1] != 'DISCOUNTED TRIAL':
                transparency_log_3.append(hard_low_contrast_current)
                hard_low_contrast_current += result[0]
                response_times_3.append(result[1])
                i += 1
            else:
                invalid_trials += 1

        elif i in hard_high_contrast:
            logging.warn("HARD HIGH CONTRAST")
            transparencies = [0.016 * (n + 1) for n in range(60)]
            transparencies = map(lambda n: n * hard_high_contrast_current,
                                 transparencies)
            result = step(window, transparencies, img_2_high_contrast, frames,
                          hard_high_contrast.index(i))
            if result[1] != 'DISCOUNTED TRIAL':
                transparency_log_4.append(hard_high_contrast_current)
                hard_high_contrast_current += result[0]
                response_times_4.append(result[1])
                i += 1
            else:
                invalid_trials += 1

        # ensures that transparencies stay between 0 and 1
        if easy_low_contrast_current > 1:
            easy_low_contrast_current = 1
        if easy_low_contrast_current < 0:
            easy_low_contrast_current = 0
        if easy_high_contrast_current > 1:
            easy_high_contrast_current = 1
        if easy_high_contrast_current < 0:
            easy_high_contrast_current = 0
        if hard_low_contrast_current > 1:
            hard_low_contrast_current = 1
        if hard_low_contrast_current < 0:
            hard_low_contrast_current = 0
        if hard_high_contrast_current > 1:
            hard_high_contrast_current = 1
        if hard_high_contrast_current < 0:
            hard_high_contrast_current = 0

        img_1_low_contrast.setOpacity(easy_low_contrast_current)
        img_1_high_contrast.setOpacity(easy_high_contrast_current)
        img_2_low_contrast.setOpacity(hard_low_contrast_current)
        img_2_high_contrast.setOpacity(hard_high_contrast_current)

        log_message = "Transparencies:" + str(easy_low_contrast_current) + \
            + ", " + str(easy_high_contrast_current) + ", " + \
            str(hard_low_contrast_current) + ", " + \
            str(hard_high_contrast_current)

        logging.warn(log_message)
        logging.flush()

    # Wrapping up experiment - undraw everything on screen, and create logs
    box_1.setAutoDraw(False)
    box_2.setAutoDraw(False)
    fixation_dot_1.setAutoDraw(False)
    fixation_dot_2.setAutoDraw(False)

    window.flip()

    transparency_logs = [transparency_log_1,
                         transparency_log_2,
                         transparency_log_3,
                         transparency_log_4]

    response_time_logs = [response_times_1,
                          response_times_2,
                          response_times_3,
                          response_times_4]

    return [response_time_logs, transparency_logs, visible_seen,
            invisible_seen, invalid_trials]


def create_subject_log(subject_number, response_times, transparency_logs,
                       visible_seen, invisible_seen, invalid_trials):

    """
    Writes the subject log. This shouldn't need to be changed
    """

    filename = "subject logs/subject {}.csv".format(subject_number)

    with open(filename, 'wb') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)

        header = ["Trial number", "Transparency", "Response time",
                  "Transparency", "Response time", "Transparency",
                  "Response time", "Transparency", "Response time"]
        wr.writerow(header)

        for i in range(len(response_times[1])):
            row = [i+1, transparency_logs[0][i], response_times[0][i],
                   transparency_logs[1][i], response_times[1][i],
                   transparency_logs[2][i], response_times[2][i],
                   transparency_logs[3][i], response_times[3][i]]
            wr.writerow(row)

    with open('subject logs/catch trials.csv', 'ab') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)

        data = [subject_number, visible_seen, invisible_seen, invalid_trials]

        wr.writerow(data)


def main(trial):

    window = trial.window

    dominant_eye = trial.dominant_eye
    pair_num = trial.pair_num

    images = trial.image_pair.images

    results = staircase(window, images, dominant_eye)

    response_times = results[0]

    transparency_logs = results[1]

    visible_seen = results[2]
    invisible_seen = results[3]
    invalid_trials = results[4]

    create_subject_log(trial.subject_number, response_times, transparency_logs,
                       visible_seen, invisible_seen, invalid_trials)

if __name__ == "__main__":
    main()
