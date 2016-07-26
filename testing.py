from psychopy import visual, core, event
from random import sample
from helpers import choose_pair, retrieve_subject_pairs, get_subject_info
import os


def step(window, transparency, img, frames):

    img.setOpacity(transparency)

    for frameN in range(60):

        frame_num = frameN//6
        mask_frame = frames[frame_num]

        mask_frame.draw()
        window.flip()

    keys = event.waitKeys(maxWait = 2)
    if keys:
        return -0.025
    else:
        return 0.025



def staircase(window, transparency):
    """
    Performs a single staircase to find the threshold of visibility for a
    subject

    returns the threshold
    """

    # Image stuff
    img = visual.ImageStim(window,
                           image="Pairs/Pair 1/1.png",
                           color=(1,1,1),
                           size = [160,160],
                           pos = (-125,0),
                           opacity = transparency)

    img.setAutoDraw(True)


    frame_paths = ["Masks/" + file for file in os.listdir("Masks")]
    frames = map(lambda file_name: visual.ImageStim(window,
                                                    image = file_name,
                                                    color = (1,1,1),
                                                    size = [160, 160],
                                                    pos = (125,0)), frame_paths)

    for i in range(10):
        transparency += step(window, transparency, img, frames)
    return transparency


def main():
    #TODO: Do we need the list of names? Maybe for recording the results?
    #TODO: Figure how csv will be formatted. Info to save:
    #   * Subject number
    #   * Response time
    #   * Difficulty of name (Just record names instead and do in post?)

    mywin = visual.Window([1920,1080],
                          monitor = "testMonitor",
                          units = "pix",
                          rgb=(-1,-1,-1),
                          fullscr = True)
    staircase(mywin, 0)



if __name__ == "__main__":
    main()
