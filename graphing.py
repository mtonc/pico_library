from picographics import PicoGraphics, DISPLAY_INKY_PACK

# Display
graphics = PicoGraphics(DISPLAY_INKY_PACK, rotate=180)
WIDTH, HEIGHT = graphics.get_bounds()
graphics.set_update_speed(2)
x_offset = int(WIDTH / 2)
y_offset = int(HEIGHT / 2)

graphics.set_pen(15)
graphics.clear()
graphics.set_pen(0)
graphics.update()


graphics.line(x_offset, HEIGHT, x_offset, 0, 2)
graphics.line(0, y_offset, WIDTH, y_offset, 2)
graphics.update()


def getPoints(func):
    points = [];
    for x in range(WIDTH):
        result = func(x)
        points.append([ x, result ])
    return points

def graph(points):
    for x, y in points:
        print(x,y)
        graphics.set_thickness(2)
        graphics.pixel(x,y)
    graphics.update()
        
def func(x):
    y = x - x_offset
    return y

graph(getPoints(func))