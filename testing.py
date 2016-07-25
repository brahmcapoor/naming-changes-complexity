from psychopy import visual, core
from random import sample
from helpers import choose_pair, retrieve_subject_pairs, get_subject_info


def step(window, transparency):
    for i in range(10):

        # Mask stuff
        frame_num = i % 10
        frame_path = "Masks/{}.JPG".format(frame_num)
        mask_frame = visual.ImageStim(window, image = frame_path, color=(1,1,1),
                               size=[160,160], pos =(125,0))


        # Image stuff
        img = visual.ImageStim(window, image="Pairs/Pair 1/1.png", color=(1,1,1),
                               size = [160,160], pos = (-125,0), opacity = transparency)

        mask_frame.draw()
        img.draw()
        window.flip()
        core.wait(0.1, 0.1)
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

    mywin = visual.Window([1920,1080], monitor = "testMonitor",
                          units = "pix", rgb=(-1,-1,-1), fullscr = True)
    staircase(mywin, 0)



if __name__ == "__main__":
    main()
