from psychopy import visual

class Image:

    default_window = visual.Window([1680,1050],
                          monitor = "testMonitor",
                          units = "pix",
                          rgb=(-1,-1,-1),
                          fullscr = True)

    def init(self, path, name):
        self.path = path
        self.name = name

    def draw(self, window = default_window, position = (0,0), size = 130, transparency = 1):

        image = visual.ImageStim(window = window,
                                 image = self.path,
                                 color = (1,1,1),
                                 size = [size, size],
                                 pos = position,
                                 opacity  = transparency)

        image.draw()

    def draw_label(self, window, position, fontsize = 50):

        label = visual.TextStim(window = window,
                                text = self.name,
                                pos = position,
                                alignHoriz = 'center',
                                alignVert = 'center',
                                height = 'fontsize')

        label.draw()


class ImagePair:

    def init(self, path, name_pair):
        
        self.img_1 = Image(path + "1.png", name_pair[0])
        self.img_2 = Image(path + "2.png", name_pair[1])
