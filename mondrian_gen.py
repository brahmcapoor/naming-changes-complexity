import random
import time
import turtle

"""
Generates circular mondrians. You shouldn't need to change this so comments
are relatvely sparse.
"""

turtle.setup(200, 200)

win = turtle.Screen()
win.screensize(200, 200)


def generate_mondrian(centers):
    t = turtle.Pen()
    t.pencolor('black')
    t.ht()
    last_color = None
    colors = {
        (1, 0, 0): "Red",
        (0, 0, 1): "Blue",
        (1, 1, 0): "Yellow"
    }
    for center in centers:
        t.up()
        t.goto(center)
        t.down()

        while True:
            color = random.choice(list(colors.keys()))
            if color != last_color:
                last_color = color
                break

        t.fillcolor(color)
        radius = random.choice([30, 40, 50, 60])

        t.begin_fill()
        t.circle(radius)  # draw a circle of random radius
        t.end_fill()


for i in range(10):
    centers = [(40 * i + 20, 40*j+20) for i in range(-3, 3)
               for j in range(-3, 3)]
    random.shuffle(centers)
    generate_mondrian(centers)
    input("Press enter to continue")
    turtle.clearscreen()
