# Simple enough, just import everything from tkinter.
"""from tkinter import *
from tkinter.tkk as t

# Here, we are creating our class, Window, and inheriting from the Frame
# class. Frame is a class from the tkinter module. (see Lib/tkinter/__init__)
class Window(Frame):

    # Define settings upon initialization. Here you can specify
    def __init__(self, master=None):
        # parameters that you want to send through the Frame class.
        Frame.__init__(self, master)

        # reference to the master widget, which is the tk window
        self.master = master

        # with that, we want to then run init_window, which doesn't yet exist
        self.init_window()

    # Creation of init_window
    def init_window(self):
        # changing the title of our master widget
        self.master.title("GUI")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        # creating a menu instance
        menu = Menu(self.master)
        self.master.config(menu=menu)

        # create the file object)
        file = Menu(menu)

        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        file.add_command(label="Exit", command=self.client_exit)

        # added "file" to our menu
        menu.add_cascade(label="File", menu=file)

        # create the file object)
        edit = Menu(menu)

        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        edit.add_command(label="Undo")

        # added "file" to our menu
        menu.add_cascade(label="Edit", menu=edit)

        # creating a button instance
        quitButton = Button(self, text="Quit", command=self.client_exit, fg='red')

        # placing the button on my window
        self.helloButton = Button(self, text="Hello", command=self.say_hi, background='red')
        self.helloButton.grid(row = 2, column = 2, sticky = W)

    def client_exit(self):
        exit()

    def say_hi(self):
        self.helloButton.configure(background= 'blue')
        print("working")


# root window created. Here, that would be the only window, but
# you can later have windows within windows.
root = Tk()

root.geometry("400x300")

# creation of an instance
app = Window(root)

# mainloop
root.mainloop()"""

'''ttk_button_label1.py
a look at foreground/background colors
'''

try:
    # Python27
    import Tkinter as tk
    import ttk
except ImportError:
    # Python31+
    import tkinter as tk
    import tkinter.ttk as ttk

root = tk.Tk()

# typical tk button
tk_btn = tk.Button(text="tk_Sample", bg='black', fg='red')
tk_btn.pack(pady=10)

# now a ttk button with styling (bg/fg won't do)
ttk.Style().configure("RB.TButton", foreground='red', background='black')
ttk_btn = ttk.Button(text="ttk_Sample", style="RB.TButton")
ttk_btn.pack(pady=10)

# foreground/background works with a ttk label but not a ttk button
# the way you expect
style = ttk.Style()
style.configure("GB.TLabel", foreground="green", background="blue")
ttk_label = ttk.Label(text="ttk_Label", style="GB.TLabel")
ttk_label.pack(pady=10)

root.mainloop()