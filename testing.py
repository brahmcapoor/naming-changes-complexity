from psychopy import visual, core, gui
from random import sample
from helpers import choose_pair, retrieve_subject_pairs

def get_subject_info():
    """
    Gets subject info and returns it as a dict
    """
    #TODO: What information is needed?

    subject_info = {
                    'Subject number': ''
                    }
    dlg = gui.DlgFromDict(dictionary = subject_info, title = "Subject info")
    return subject_info

def main():

    subject_info = get_subject_info()
    pair_nums, names = retrieve_subject_pairs(int(subject_info['Subject number']))

    for pair in pair_nums:
        pair_path = choose_pair(pair)

if __name__ == "__main__":
    main()
