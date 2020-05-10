from tkinter import *
from tkinter import ttk
import time
from ctypes import windll
from pyautogui import size, screenshot
from cfg_module import cfg_load, cfg_save


def name_file():
    '''Create File name'''
    now = time.time()
    name = time.strftime("%d%H%M%S", time.gmtime(now))
    return name


def take_shot(PATH, coords=None):
    '''Create Fullscreen screenshot'''
    print('saving to -> {}'.format(PATH))
    if coords != None:
        img = screenshot(region=coords)
    else:
        img = screenshot()
    img.save(PATH + '\\' + name_file() + '.png')
    return 1


def res_check():
    '''Resize screen shot for high resolution (bug tkinter resolution)'''
    w, h = size()
    if h == 1080 and w == 1920:
        return True
    else:
        return False


class DrawingBox:
    def __init__(self, box):
        # Frame.__init__(self, master=master)
        self.box = box
        # self.pack()
        self.height, self.width = self.box.winfo_screenheight(), self.box.winfo_screenwidth()
        print(self.height, self.width)
        self.canvas = Canvas(self.box, width=self.width, height=self.height)

        self.l1 = ttk.Label(self.box, text='Select window region')
        self.l1.config(font=("Arial", 44))
        lh = self.height
        self.l1.pack(pady=lh / 3)

        self.box.bind("<Button-1>", self.on_button_press)
        self.box.bind("<B1-Motion>", self.on_move_press)
        self.box.bind("<ButtonRelease-1>", self.on_button_release)
        self.box.bind("<Escape>", self.exit)
        self.box.focus_set()

        self.selection = None
        self.start_x = None
        self.start_y = None
        self.postions = ()

    def on_button_press(self, event):
        self.l1.pack_forget()
        self.canvas.pack()
        # save mouse drag start position
        self.start_x = event.x
        self.start_y = event.y

        self.selection = self.canvas.create_rectangle(event.x, event.y, event.x + 1, event.y + 1, width=4)

    def on_move_press(self, event):
        # print('mouse moving... ', event.x, event.y)
        self.curX, self.curY = (event.x, event.y)
        # expand rectangle as you drag the mouse

        self.canvas.coords(self.selection, self.start_x, self.start_y, self.curX, self.curY)

    def on_button_release(self, event):
        # print(self.start_x, self.start_y, self.curX, self.curY)

        if self.start_x > event.x:
            x1, x2 = event.x, self.start_x - event.x
        else:
            x1, x2 = self.start_x, event.x - self.start_x
        if self.start_y > event.y:
            y1, y2 = event.y, self.start_y - event.y
        else:
            y1, y2 = self.start_y, event.y - self.start_y

        # print(x1,y1,x2,y2)

        self.postions = (x1, y1, x2, y2)
        self.canvas.pack_forget()
        self.canvas.delete('all')
        self.box.destroy()

    def getter(self):
        return self.postions

    def exit(self, event):
        self.box.destroy()
        self.postions = (0, 0, 0, 0)


def draw_box(PATH, mode=2):
    '''main function of drawed box'''

    box = Tk()
    box.focus_get()
    box.focus_displayof()
    box.attributes("-topmost", True)

    width, height = box.winfo_screenwidth(), box.winfo_screenheight()
    box.geometry("%dx%d+0+0" % (width, height))
    box.attributes("-fullscreen", True)
    box.attributes("-alpha", 0.2)

    box.overrideredirect(1)
    DB = DrawingBox(box)
    box.mainloop()
    positions = DB.getter()

    user32 = windll.user32
    user32.SetProcessDPIAware()

    del DB
    if positions != (0, 0, 0, 0):
        if mode == 1:
            img = screenshot(region=positions)
            img.save(PATH + '\\' + name_file() + '.png')
        elif mode == 2:
            settings = cfg_load()
            settings[7] = positions
            cfg_save(settings)

    return 1

# draw_box('C:\\Users\\Patryk\\Desktop')
