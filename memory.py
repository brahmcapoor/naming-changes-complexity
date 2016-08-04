from psychopy import visual, core, event
from psychopy.visual import ImageStim, TextStim
from helpers import retrieve_subject_info, choose_pair, get_user_input
import os, csv


def test_image(window, name, image):
    image = ImageStim(win = window,
                      image = image,
                      color = (1,1,1),
                      size = [200, 200],
                      pos = (0,0))

    image.setAutoDraw(True)
    window.flip()

    name = get_user_input(window, (0,-150))
    return name


def write_to_csv(new_experiment, subject_number, name_1, remembered_name_1,
                 name_2, remembered_name_2):

    if new_experiment:
        if os.path.exists("memory_results.csv"):
            os.remove("memory_results.csv")

    data = [subject_number, name_1, remembered_name_1, name_2,
            remembered_name_2]

    with open("memory_results.csv", 'ab') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_ALL)

        if new_experiment:
            header = ["Subject Number", "Name 1", "Remembered Name 1", "Name 2", "Remembered Name 2"]
            wr.writerow(header)

        wr.writerow(data)




def main(window, trial):

    subject = retrieve_subject_info(subject_number)
    pair_num = subject[3]
    name_1 = subject[4]
    name_2 = subject[5]

    pair_path = choose_pair(pair_num)
    img_1 = pair_path + "1.png"
    img_2 = pair_path + "2.png"

    remembered_name_1 = test_image(window, name_1, img_1)
    remembered_name_2 = test_image(window, name_2, img_2)

    write_to_csv(new_experiment = new_experiment,
                 subject_number = subject_number,
                 name_1 = name_1,
                 remembered_name_1 = remembered_name_1,
                 name_2 = name_2,
                 remembered_name_2 = remembered_name_2)



if __name__ == '__main__':
    main()
