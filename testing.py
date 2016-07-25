from psychopy import visual, core
from random import sample
from helpers import choose_pair, retrieve_subject_pairs, get_subject_info


def main():
    #TODO: Do we need the list of names? Maybe for recording the results?
    #TODO: Figure how csv will be formatted. Info to save:
    #   * Subject number
    #   * Response time
    #   # Difficulty of name (Just record names instead and do in post?)

    mywin = visual.Window([1920,1080], monitor = "testMonitor",
                          units = "deg", rgb=(-1,-1,-1), fullscr = True)
    for i in range(100):
        img_num = i % 10
        img_path = "Masks/{}.JPG".format(img_num)
        img = visual.ImageStim(mywin, image = img_path, color=(1,1,1),
                               size=[5,5], pos =(0,0))
        img.draw()
        mywin.flip()
        core.wait(0.1)

if __name__ == "__main__":
    main()
