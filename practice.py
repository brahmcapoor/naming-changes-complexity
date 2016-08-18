from psychopy import visual, event
from psychopy.visual import ImageStim, Rect, Circle
from experiment_objects import Image
from testing import step
import os


def main(window, dominant_eye):

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


    transparencies = [0.016 * (n + 1) for n in range(60)]

    img = Image("Pairs/practice_img.jpg", "")

    img = img.stimulus(window,
                       position = (-1*maskPos, 150),
                       transparency = 1)

    for i in range(10):
        step(window, transparencies, img, frames, 1)

    box_1.setAutoDraw(False)
    box_2.setAutoDraw(False)

    fixation_dot_1.setAutoDraw(False)
    fixation_dot_2.setAutoDraw(False)




if __name__ == '__main__':
    main()
