from psychopy import visual, core
from random import sample
from helpers import choose_pair, retrieve_subject_pairs, get_subject_info


def main():
    #TODO: Do we need the list of names? Maybe for recording the results?
    #TODO: Figure how csv will be formatted. Info to save:
    #   * Subject number
    #   * Response time
    #   # Difficulty of name (Just record names instead and do in post?)

    subject_info = get_subject_info()
    pair_nums, names = retrieve_subject_pairs(subject_info)

    for pair in pair_nums:
        pair_path = choose_pair(pair)

if __name__ == "__main__":
    main()
