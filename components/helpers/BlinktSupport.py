from blinkt import set_brightness, set_pixel, show, clear


class Blinkt:
    """
    This is a simple class for modules to make use of blinkt if they wish
    """
    def __init__(self, red=30, green=30, blue=30, brightness=0.1):
        self.colours = [red, green, blue]
        set_brightness(brightness)

    def __exit__(self):
        self.clear()

    @staticmethod
    def unset_pixel(pixel):
        set_pixel(pixel, 0, 0, 0)
        show()
        return

    def set_pixel(self, pixel):
        set_pixel(pixel, self.colours[0], self.colours[1], self.colours[2])
        show()
        return

    @staticmethod
    def clear():
        clear()
        show()

    @staticmethod
    def new_brightness(brightness):
        set_brightness(brightness)
        return

    def new_colours(self, red, green, blue):
        self.colours = [red, green, blue]
        return

    def new_colors(self, red, green, blue):
        self.new_colours(red, green, blue)
        return
