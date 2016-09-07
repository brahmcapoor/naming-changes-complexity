import training
import memory
import testing


class Image():

    def __init__(self, path, name):
        self.path = path
        self.name = name

    def stimulus(self, window, position=(0, 0), size=130, transparency=1):

        image = visual.ImageStim(win=window,
                                 image=self.path,
                                 color=(1, 1, 1),
                                 size=[size, size],
                                 pos=position,
                                 opacity=transparency)

        return image

    def label(self, window, position, fontsize=50):

        label = visual.TextStim(win=window,
                                text=self.name,
                                pos=position,
                                alignHoriz='center',
                                alignVert='center',
                                height=fontsize)

        return label

    def foil(self, window, position=(0, 0), size=200):
        foil_path = self.path[:-4] + "_mask.png"

        foil = visual.ImageStim(win=window,
                                image=foil_path,
                                color=(1, 1, 1),
                                size=[size, size],
                                pos=position)

        return foil


class Subject():

    def __init__(self, window, round_number, dominant_eye, images):
        self.window = window
        self.round_Number = round_number
        self.dominant_eye = dominant_eye
        self.images = image

    def train(self):
        training.main(self)

    def memory_test_first(self):
        memory.main(self)

    def test(self):
        testing.main(self)

    def memory_test_second(self):
        memory.main(self, True)
