from psychopy import visual, core, event
from psychopy.visual import ImageStim, TextStim
from helpers import retrieve_subject_info, choose_pair

def get_user_input(window, name):


    input_name = ""
    user_input = TextStim(win = window,
                          text = input_name,
                          pos = (0, -150))

    user_input.setAutoDraw(True)
    window.flip()

    while True:
        char = event.waitKeys()[0]
        if char.isalpha() and len(char) == 1:
            input_name += char
        if char ==  'return':
            user_input.setAutoDraw(False)
            window.flip()
            return input_name
        if char == 'comma':
            input_name = input_name[:-1]


        user_input.text = input_name
        window.flip()



def test_image(window, name, image):
    image = ImageStim(win = window,
                      image = image,
                      color = (1,1,1),
                      size = [200, 200],
                      pos = (0,0))

    image.setAutoDraw(True)
    window.flip()

    name = get_user_input(window, name)
    #TODO: compare user_input and write to file
    #TODO: figure out what to write to file


def main(window, subject_number):

    subject = retrieve_subject_info(subject_number)
    pair_num = subject[3]
    name_1 = subject[4]
    name_2 = subject[5]

    pair_path = choose_pair(pair_num)
    img_1 = pair_path + "1.png"
    img_2 = pair_path + "2.png"

    test_image(window, name_1, img_1)
    test_image(window, name_2, img_2)



if __name__ == '__main__':
    main()
