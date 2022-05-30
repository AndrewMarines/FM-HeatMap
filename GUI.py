# Multi-frame tkinter application v2.3
import shutil
import tkinter as tk
import Utils
from PIL import Image, ImageTk
import glob
import os
import cv2
import time
import easygui
import subprocess
import configparser

CONF_FILE = "labels.txt"
configlabels = configparser.ConfigParser()
def save_labels():

    configlabels['DEFAULT'] = {
        'NO_SCREEN_AVAILABLE': """No screenshots available. Choose where you wish to return.""",
        'REMOVE_FROM_DISK': "Delete file from drive",
        'REMOVE_FROM_QUEUE': "Remove screenshot from queue",
        'SAVE_HEATMAP': "Save heatmap",
        'GENERAL_DIRECTORY': "Open program folder",
        'QUEUE_DIRECTORY': "Open screenshots folder",
        'RELOAD_SCREEN': "Reload screen",
        'PIXEL_COLOURATION': "Pixel colour",
        'INTENSITY': "Pixel intensity",
        'ATTACKING_DIRECTION': "Direction of attack",
        'SCREENSHOT': 'Screenshot',
        'HOMEPAGE': "Home",
        'HEATMAP': "Heatmap",
        'DEFAULT_HEATMAP_NAME': "Heatmap",
        'NUMBER_OF_SCREENSHOT': "NUMBER OF SCREENSHOTS",
        'SECONDS_PER_SCREENSHOT': "Frequency of screenshot",
        'START': "Start",
        'MATCH_NAME' : "Folder name",
        'STOP_SCREENSHOTTING' : " TO STOP"

    }
    with open(CONF_FILE, 'w') as configfile:
        configlabels.write(configfile)

def readlabels():
    global NO_SCREEN_AVAILABLE, REMOVE_FROM_DISK, REMOVE_FROM_QUEUE, SAVE_HEATMAP, GENERAL_DIRECTORY, QUEUE_DIRECTORY, RELOAD_SCREEN, STOP_SCREENSHOTTING
    global PIXEL_COLOURATION, INTENSITY, ATTACKING_DIRECTION, SCREENSHOT, HOMEPAGE, HEATMAP, DEFAULT_HEATMAP_NAME, NUMBER_OF_SCREENSHOT,SECONDS_PER_SCREENSHOT, START,MATCH_NAME
    if glob.glob(CONF_FILE):
        configlabels.read(CONF_FILE)
        NO_SCREEN_AVAILABLE = configlabels['DEFAULT']['NO_SCREEN_AVAILABLE']
        REMOVE_FROM_DISK = configlabels['DEFAULT']['REMOVE_FROM_DISK']
        REMOVE_FROM_QUEUE = configlabels['DEFAULT']['REMOVE_FROM_QUEUE']
        SAVE_HEATMAP = configlabels['DEFAULT']['SAVE_HEATMAP']
        GENERAL_DIRECTORY = configlabels['DEFAULT']['GENERAL_DIRECTORY']
        QUEUE_DIRECTORY = configlabels['DEFAULT']['QUEUE_DIRECTORY']
        RELOAD_SCREEN = configlabels['DEFAULT']['RELOAD_SCREEN']
        PIXEL_COLOURATION = configlabels['DEFAULT']['PIXEL_COLOURATION']
        INTENSITY = configlabels['DEFAULT']['INTENSITY']
        ATTACKING_DIRECTION = configlabels['DEFAULT']['ATTACKING_DIRECTION']
        SCREENSHOT = configlabels['DEFAULT']['SCREENSHOT']
        HOMEPAGE = configlabels['DEFAULT']['HOMEPAGE']
        HEATMAP = configlabels['DEFAULT']['HEATMAP']
        DEFAULT_HEATMAP_NAME = configlabels['DEFAULT']['DEFAULT_HEATMAP_NAME']
        NUMBER_OF_SCREENSHOT = configlabels['DEFAULT']['NUMBER_OF_SCREENSHOT']
        SECONDS_PER_SCREENSHOT = configlabels['DEFAULT']['SECONDS_PER_SCREENSHOT']
        START = configlabels['DEFAULT']['START']
        MATCH_NAME = configlabels['DEFAULT']['MATCH_NAME']
        STOP_SCREENSHOTTING = configlabels['DEFAULT']['STOP_SCREENSHOTTING']
    else:
        print("NO CONFIG FILE, CREATING A DEFAULT ONE")
        save_labels()

class GUI_APP(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(Home)
        self.iconbitmap('src//icon.ico')

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame

        self._frame.pack()


class Home(tk.Frame):


    def __init__(self, master):
        tk.Frame.__init__(self, master)
        master.title("HOMEPAGE")

        # SCREENSHOT SECTION
        screenshot_icon = tk.PhotoImage(file="src/screenshot.png")
        screenshot_icon = screenshot_icon.subsample(3, 3)
        ss = tk.Button(self, text=SCREENSHOT, image=screenshot_icon,
                       compound=tk.TOP, command=lambda: master.switch_frame(Screenshot), background="#ffffff")
        ss.image = screenshot_icon
        ss.pack(side=tk.LEFT)

        # HEATMAP SECTION
        heatmap_icon = tk.PhotoImage(file="src/heatmap.png")
        heatmap_icon = heatmap_icon.subsample(3, 3)
        hm = tk.Button(self, text='Heatmap', image=heatmap_icon,
                       compound=tk.TOP, command=lambda: [Utils.organize_images(), master.switch_frame(Elaborazione)],
                       background="#ffffff")
        hm.image = heatmap_icon
        hm.pack()




class Screenshot(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        master.title(SCREENSHOT)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        tk.Button(self, text=HOMEPAGE, command=lambda: master.switch_frame(Home), background="#ffffff").grid(
            row=0, column=0, sticky=tk.NW)

        # SPINBOXES
        tk.Label(self, text=SECONDS_PER_SCREENSHOT).grid(row=1, column=0, padx=5)
        var_ts = tk.IntVar(self)
        var_ts.set(Utils.ingame_seconds_per_screenshot)
        TS = tk.Spinbox(self, from_=1, to=5000, textvariable=var_ts)
        TS.grid(row=1, column=1, padx=5)
        var_ns = tk.IntVar(self)
        var_ns.set(Utils.number_of_screenshot)
        tk.Label(self, text = NUMBER_OF_SCREENSHOT).grid(row=2, column=0, padx=5)
        NS = tk.Spinbox(self, from_=1, to=200, textvariable=var_ns)
        NS.grid(row=2, column=1, padx=5, pady=70)

        match_name = tk.StringVar(self)
        match_name.set(Utils.get_time())
        tk.Label(self, text=MATCH_NAME).grid(row=3, column=0, padx=5)
        match_name_entry = tk.Entry(self, textvariable=match_name)
        match_name_entry.grid(row = 3, column = 1, padx = 5)

        # PREVIEW
        img = Image.fromarray(Utils.ant_screenshot())
        img_Screenshot = ImageTk.PhotoImage(image=img)
        img_Screenshot = img_Screenshot._PhotoImage__photo.subsample(2, 2)
        Screen = tk.Button(self, image=img_Screenshot, command=lambda: [
            master.iconify(),
            time.sleep(0.5),
            Utils.find_coords(master),
            self.master.switch_frame(Home)
        ])
        Screen.image = img_Screenshot
        Screen.grid(row=0, column=2, padx=20, pady=20, rowspan=5)
        textavvio= START + "(" + Utils.get_Stop_Key() + " "+ STOP_SCREENSHOTTING + ")"
        avvio = tk.Button(self, text=textavvio,
                          command=lambda: [
                              Utils.set_Time_Screen(var_ts.get()),
                              Utils.set_Number_Screenshot(var_ns.get()),
                              Utils.screenshot(master, match_name.get()),
                              Utils.organize_images(),
                              master.state('normal'),
                              master.switch_frame(Elaborazione)
                          ])
        avvio.grid(row=6, columnspan=10, pady=10, sticky=tk.NSEW)


class Elaborazione(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        master.title(HEATMAP)
        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff", width=700, height=700)
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.settings = tk.Frame(self, background="#ffffff")
        self.canvas.grid_rowconfigure(0, weight=1)
        self.canvas.grid_columnconfigure(0, weight=1)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.canvas.grid(row=0, column=0, sticky=tk.NSEW)
        self.vsb.grid(row=0, column=1, sticky=tk.NSEW)
        self.settings.grid(row=0, column=2, sticky=tk.NSEW)

        self.canvas.create_window((4, 4), window=self.frame, anchor="nw",
                                  tags="self.frame")
        self.frame.bind("<Configure>", self.onFrameConfigure)
        self.populate()

        tk.Button(self, text = START, command=lambda: [
            Utils.set_Pixel_Intensity(var_pix_int.get()),
            Utils.set_Around_Pixel_Intensity(var_pix_int_vic.get()),
            Utils.readconfig(),
            self.heatmap_finale(variable.get())
        ]).grid(row=1, columnspan=3, sticky=tk.NSEW)

        var_pix_int = tk.IntVar(self)
        var_pix_int.set(Utils.intensita_pixel)
        tk.Button(self.settings, text=HOMEPAGE, command=lambda: master.switch_frame(Home), background="#ffffff").grid(
            row=0, column=0, pady=5)

        tk.Label(self.settings, text=INTENSITY, background="#ffffff").grid(row=1, column=0, sticky=tk.NSEW)
        PI = tk.Spinbox(self.settings, from_=1, to=5, textvariable=var_pix_int, background="#ffffff")
        PI.grid(row=2, column=0, padx=5, sticky=tk.NSEW)
        var_pix_int_vic = tk.IntVar(self)
        var_pix_int_vic.set(Utils.intensita_p_vicini)
        tk.Label(self.settings, text=PIXEL_COLOURATION, background="#ffffff").grid(row=3, column=0,
                                                                                   sticky=tk.NSEW)
        PI_V = tk.Spinbox(self.settings, from_=0, to=5, textvariable=var_pix_int_vic, background="#ffffff")
        PI_V.grid(row=4, column=0, padx=5, sticky=tk.NSEW)
        tk.Button(self.settings, text=RELOAD_SCREEN, command=self.reload, background="#ffffff").grid(row=5, column=0,
                                                                                                     sticky=tk.NSEW, pady=5)
        tk.Button(self.settings, text =QUEUE_DIRECTORY, background="#ffffff", command = lambda : subprocess.Popen('explorer "elab_movimenti"')).grid(row=6, column=0, sticky=tk.NSEW, pady=5)
        tk.Button(self.settings, text =GENERAL_DIRECTORY, background="#ffffff", command = lambda : subprocess.Popen('explorer "movimenti"')).grid(row=7, column=0, sticky=tk.NSEW, pady=5)

        #ATTACKING DIRECTION
        DIRECTION = [
            "NONE",
            "LEFT",
            "RIGHT"
        ]
        variable = tk.StringVar(master)
        variable.set(DIRECTION[0])  # default value
        tk.Label(self.settings, text =ATTACKING_DIRECTION, background="#ffffff").grid(row=7, column=0, sticky=tk.NSEW)
        MENU_DIRECTION = tk.OptionMenu(self.settings, variable, *DIRECTION).grid(row=8, column=0, sticky=tk.NSEW)

    def heatmap_finale(self, direction):
        def salva_heatmap(img):
            f_out = easygui.filesavebox("Select an output file", title=SAVE_HEATMAP, default=DEFAULT_HEATMAP_NAME,
                                        filetypes=".png")
            if ".png" in f_out:
                cv2.imwrite(f_out, img)
            else:
                cv2.imwrite(f_out + ".png", img)

        top = tk.Toplevel()
        top.title(HEATMAP)
        original_img = Utils.generazione_heatmap()
        height = original_img.shape[0]
        width = original_img.shape[1]
        color = (0, 0, 255)
        thickness = 9
        if (direction == "RIGHT"):
            start_point = (int(width / 2 - 100), 25)
            end_point = (int(width / 2 + 100), 25)

            original_img = cv2.arrowedLine(original_img, start_point, end_point,
                                           color, thickness)
        elif (direction == "LEFT"):
            start_point = (int(width / 2 + 100), 20)
            end_point = (int(width / 2 - 100), 20)


            original_img = cv2.arrowedLine(original_img, start_point, end_point,
                                           color, thickness)
        blue, green, red = cv2.split(original_img)
        img = cv2.merge((red, green, blue))

        img = Image.fromarray(img)
        img_Screenshot = ImageTk.PhotoImage(image=img)
        # Create a Label to display the image
        tk.Label(top, image=img_Screenshot).grid(row=0, column=0)
        tk.Button(top, text=SAVE_HEATMAP, command=lambda: salva_heatmap(original_img)).grid(row=1, column=0)
        top.mainloop()

    def populate(self):
        btn_img = []
        btn_remove = []
        btn_rem_disk = []
        path = "elab_movimenti"

        directories = glob.glob(path + "/*/", recursive=True)
        all_images = glob.glob(path + "/**/*.png", recursive=True)


        ants = []
        btn_remove_dir = []
        padx = 10
        pady = 10
        index = 0
        if len(all_images) == 0:
            self.no_screenshot()
        if len(directories) == 0:
            directories.append(path)
        for f in all_images:
            contenuto = False
            for d in directories:
                if(d in f):
                    contenuto = True
            if(not contenuto):
                if not os.path.exists(path + '/DEFAULT'):
                    os.mkdir(path + '/DEFAULT')
                shutil.move(f, path + '/DEFAULT')
        all_images = glob.glob(path + "/**/*.png", recursive=True)
        index_dir = -1
        for d in range(len(directories)):
            d_string = directories[d].upper()
            d_string = d_string.replace("ELAB_MOVIMENTI\\", "").replace("\\","")
            tk.Label(self.frame, text = d_string, background="#ffffff").grid(row = index_dir + 1 , column = 0)
            btn_remove_dir.append(tk.Button(self.frame, text =REMOVE_FROM_QUEUE, command= lambda c = d: [shutil.rmtree(directories[c]),
                                                                                                         self.refresh()]))
            btn_remove_dir[d]. grid(row = index_dir + 1 , column = 1, columnspan= 2, sticky = tk.NSEW)


            images = glob.glob(directories[d] + '/*.png')

            for i in range(len(images)):
                ants.append(tk.PhotoImage(file=all_images[index]))
                ants[index] = ants[index].subsample(3, 3)
                btn_img.append(tk.Button(self.frame, text=all_images[index], image=ants[index],
                                         compound=tk.TOP, command=lambda c=index: self.getImage(c)))
                btn_remove.append(tk.Button(self.frame, text=REMOVE_FROM_QUEUE, command=lambda c=index: [
                    os.remove(all_images[c]),
                    self.refresh()
                ]))
                btn_rem_disk.append(tk.Button(self.frame, text=REMOVE_FROM_DISK, command=lambda c=index: [
                    os.remove(all_images[c]),
                    os.remove(all_images[c].replace("elab_", "")),
                    self.refresh()
                ]))
                btn_img[index].image = ants[index]
                btn_img[index].grid(row=index_dir+2, column=0, sticky=tk.NS, padx=padx, pady=pady)
                btn_remove[index].grid(row=index_dir+2, column=1, sticky=tk.NS, padx=padx, pady=pady)
                btn_rem_disk[index].grid(row=index_dir+2, column=2, sticky=tk.NS, padx=padx, pady=pady)
                index += 1
                index_dir += 2


    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))



    def getImage(self, i):

        path = "elab_movimenti"
        images = glob.glob(path + "/**/*.png", recursive=True)

        top = tk.Toplevel()
        top.title(images[i])



        image = cv2.imread(images[i])
        image_frame = tk.Frame(top, background="#ffffff")
        settings_frame = tk.Frame(top, background="#ffffff")
        blue, green, red = cv2.split(image)
        img = cv2.merge((red, green, blue))
        img = Image.fromarray(img)
        img_Screenshot = ImageTk.PhotoImage(image=img)
        # Create a Label to display the image
        tk.Label(image_frame, image=img_Screenshot).grid(row=0, column=0)

        turn_right_icon = tk.PhotoImage(file="src/Turn_Right.png")
        turn_right_icon = turn_right_icon.subsample(3, 3)
        tr = tk.Button(settings_frame, image=turn_right_icon,
                        command=lambda: [Utils.rotate_image(image, images[i]),
                                         self.refresh(),
                                         top.destroy(),
                                         self.getImage(i)
                                         ], background="#ffffff")
        tr.image = turn_right_icon
        tr.pack(side=tk.LEFT)

        image_frame.pack(side= tk.LEFT)
        settings_frame.pack(side=tk.RIGHT)


        top.mainloop()

    def refresh(self):
        self.destroy()
        self.master.switch_frame(Elaborazione)

    def reload(self):
        self.destroy()
        Utils.organize_images()
        self.master.switch_frame(Elaborazione)

    def no_screenshot(self):
        top = tk.Toplevel()
        top.title("NO SCREENSHOT AVAILABLE")
        tk.Label(top, text=NO_SCREEN_AVAILABLE).grid(row=0, columnspan=2)
        tk.Button(top, text=HOMEPAGE, command=lambda: [self.master.switch_frame(Home), top.destroy()]).grid(row=1,
                                                                                                              column=0)
        tk.Button(top, text=SCREENSHOT, command=lambda: [self.master.switch_frame(Screenshot), top.destroy()]).grid(
            row=1, column=1)


def main():
    readlabels()
    Utils.readconfig()
    app = GUI_APP()
    app.configure(background='white')
    app.resizable(False, False)
    app.mainloop()
