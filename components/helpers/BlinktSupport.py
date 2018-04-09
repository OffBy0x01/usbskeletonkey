try:
    from blinkt import set_brightness, set_pixel, show, clear
    blinktImported = True
except ImportError:
    try:
        import pip
        pip.main(['install', '--user', 'blinkt'])
        from blinkt import set_brightness, set_pixel, show, clear
        blinktImported = True
    except ImportError:
        blinktImported = False


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
        if blinktImported:
            set_pixel(pixel, 0, 0, 0)
            show()
        return

    def set_pixel(self, pixel):
        if blinktImported:
            set_pixel(pixel, self.colours[0], self.colours[1], self.colours[2])
            show()
        return

    @staticmethod
    def clear():
        if blinktImported:
            clear()
            show()
        return

    @staticmethod
    def new_brightness(brightness):
        if blinktImported:
            set_brightness(brightness)
        return

    def new_colours(self, red, green, blue):
        self.colours = [red, green, blue]
        return

    def new_colors(self, red, green, blue):
        self.new_colours(red, green, blue)
        return

    def progressive_pixels(self, current_task, total_tasks):
        """
        Where current tasks to complete is greater than 8 this can set the status lights
        for you upon calling with correct inputs

        :param current_task: Type int
        :param total_tasks: Type int

        Can be used with less than 8 but will hypothetically miss some LED's
        """
        self.set_pixel(int((current_task / total_tasks) * 8))

        return
