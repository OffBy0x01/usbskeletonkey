from blinkt import set_brightness, set_pixel, show, clear


class Blinkt:
    """
    This is a simple class for modules to make use of blinkt if they wish
    """
    def __init__(self, red=30, green=30, blue=30, brightness=0.1):
        self.colors = [red, green, blue]
        set_brightness(brightness)

    def __exit__(self):
        clear()
        show()

    def setPixel(self, pixel):
        set_pixel(pixel, self.colors[0], self.colors[1], self.colors[2])
        show()
        return

    def newColors(self, red, green, blue):
        self.colors = [red, green, blue]
        return
