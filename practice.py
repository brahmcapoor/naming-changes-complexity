from psychopy import visual, event
from psychopy.visual import ImageStim, Rect, Circle
from experiment_objects import Image
from testing import step
from random import shuffle
import os

"""
The practice trials
"""

def main(window, dominant_eye):

    """
    This is pretty much just a less complicated version of the step method
    in the testing script, so it's not commented that much.
    """

    # Fusion box stuff

    maskPos = -200
    if dominant_eye:
        maskPos = 200


    box_1 = Rect(win = window,
                 width = 180,
                 height = 180,
                 lineWidth = 4,
                 lineColor = 'grey',
                 pos = (-200, 150),
                 autoDraw = True)

    box_2 = Rect(win = window,
                 width = 180,
                 height = 180,
                 lineWidth = 4,
                 lineColor = 'grey',
                 pos = (-1 * -200, 150),
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
                          pos = (-200, 150),
                          lineWidth = 0,
                          autoDraw = True)

    fixation_dot_2 = Circle(win = window,
                          radius = 2,
                          fillColor = 'red',
                          pos = (-1 * -200, 150),
                          lineWidth = 0,
                          autoDraw = True)



    img = Image("Pairs/practice_img.jpg", "")

    img = img.stimulus(window,
                       position = (-1*maskPos, 150),
                       transparency = 1)

    transparencies = [0.016 * (n + 1) * 0.1 for n in range(60)]

    # ten trials at 10% contrast and ten at 50%
    N_TRIALS = 20
    all_trials = [i for i in range(N_TRIALS)]
    shuffle(all_trials)

    low_contrast = all_trials[:10]
    high_contrast = all_trials[10:]

    low_transparencies = [0.016 * (n + 1) * 0.1 for n in range(60)]
    high_transparencies = [0.016 * (n + 1) * 0.5 for n in range(60)]

    for i in range(N_TRIALS):
        if i in low_contrast:
            step(window, low_transparencies, img, frames, 0.05 * i)
        if i in high_contrast:
            step(window, high_transparencies, img, frames, 0.05 * i)

    box_1.setAutoDraw(False)
    box_2.setAutoDraw(False)

    fixation_dot_1.setAutoDraw(False)
    fixation_dot_2.setAutoDraw(False)




if __name__ == '__main__':
    main()
