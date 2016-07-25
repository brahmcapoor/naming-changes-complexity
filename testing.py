from psychopy import visual, core
from random import sample
from helpers import choose_pair, retrieve_subject_pairs, get_subject_info


def mask_frame(frame_num, window):
    img_num = frame_num % 10
    img_path = "Masks/{}.JPG".format(img_num)
    img = visual.ImageStim(window, image = img_path, color=(1,1,1),
                           size=[5,5], pos =(0,0))
    img.draw()
    window.flip()
    core.wait(0.1,hogCPUperiod = 0.1)

def main():
    #TODO: Do we need the list of names? Maybe for recording the results?
    #TODO: Figure how csv will be formatted. Info to save:
    #   * Subject number
    #   * Response time
    #   # Difficulty of name (Just record names instead and do in post?)

    mywin = visual.Window([1920,1080], monitor = "testMonitor",
                          units = "deg", rgb=(-1,-1,-1), fullscr = True)
    for i in range(10):
        mask_frame(i, mywin)

if __name__ == "__main__":
    main()
