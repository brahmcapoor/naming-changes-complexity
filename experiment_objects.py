from psychopy import visual

class Image():

    def __init__(self, path, name):
        self.path = path
        self.name = name

    def stimulus(self, window, position = (0,0), size = 130, transparency = 1):

        image = visual.ImageStim(win = window,
                                 image = self.path,
                                 color = (1,1,1),
                                 size = [size, size],
                                 pos = position,
                                 opacity  = transparency)

        return image

    def label(self, window, position, fontsize = 50):

        label = visual.TextStim(win = window,
                                text = self.name,
                                pos = position,
                                alignHoriz = 'center',
                                alignVert = 'center',
                                height = fontsize)

        return label

    def foil(self, window, position = (0,0), size = 200):
        foil_path = self.path[:-4] + "_mask.png"

        foil = visual.ImageStim(win = window,
                                image = foil_path,
                                color = (1,1,1),
                                size = [size, size],
                                pos = position)

        return foil


class ImagePair():

    def __init__(self, path, name_pair):

        self.img_1 = Image(path + "1.png", name_pair[0])
        self.img_2 = Image(path + "2.png", name_pair[1])
        self.images = [self.img_1, self.img_2]

class Trial():

    def __init__(self, window, subject_number, round_number, dominant_eye,
                 image_pair,pair_num):

        self.window = window
        self.subject_number = subject_number
        self.round_number = round_number
        self.dominant_eye = dominant_eye
        self.image_pair = image_pair
        self.pair_num = pair_num
