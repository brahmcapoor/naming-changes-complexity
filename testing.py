from psychopy import visual, core
from random import sample
from helpers import choose_pair, retrieve_subject_pairs, get_subject_info
import os


def step(window, transparency):


    # Image stuff
    img = visual.ImageStim(window,
                           image="Pairs/Pair 1/1.png",
                           color=(1,1,1),
                           size = [160,160],
                           pos = (-125,0),
                           opacity = transparency)

    frame_paths = ["Masks/" + file for file in os.listdir("Masks")]
    frames = map(lambda file_name: visual.ImageStim(window,
                                                    image = file_name,
                                                    color = (1,1,1),
                                                    size = [160, 160],
                                                    pos = (125,0)), frame_paths)

    for frameN in range(60):

        frame_num = frameN//6
        frame_path = "Masks/{}.JPG".format(frame_num)
        mask_frame = frames[frame_num]

        mask_frame.draw()
        img.draw()
        window.flip()

    return 0.025



def staircase(window, transparency):
    """
    Performs a single staircase to find the threshold of visibility for a
    subject

    returns the threshold
    """
    for i in range(40):
        transparency += step(window, transparency)
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
