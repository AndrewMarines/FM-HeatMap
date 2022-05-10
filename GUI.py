# Multi-frame tkinter application v2.3
import tkinter as tk
import Utils
from PIL import Image, ImageTk
import glob
import os
import cv2
import time

class GUI_APP(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(Home)

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
        screenshot_icon = tk.PhotoImage(file="src/screenshot.png")
        screenshot_icon = screenshot_icon.subsample(3, 3)
        ss = tk.Button(self, text='Screenshot', image=screenshot_icon,
                    compound=tk.TOP, command=lambda:master.switch_frame(Screenshot), background="#ffffff")
        ss.image = screenshot_icon
        ss.pack(side=tk.LEFT)

        heatmap_icon = tk.PhotoImage(file="src/heatmap.png")
        heatmap_icon = heatmap_icon.subsample(3, 3)
        #hm = tk.Button(self, text='Heatmap', image=heatmap_icon,
        #            compound=tk.TOP, command=Utils.generazione_heatmap)
        hm = tk.Button(self, text='Heatmap', image=heatmap_icon,
                    compound=tk.TOP, command=lambda:[Utils.organize_images(), master.switch_frame(Elaborazione)], background="#ffffff")
        hm.image = heatmap_icon
        hm.pack(side=tk.RIGHT)



class Screenshot(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        master.title("SCREENSHOT")
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        tk.Button(self, text="HOMEPAGE", command=lambda: master.switch_frame(Home), background="#ffffff").grid(
            row=0, column=0,sticky=tk.NW)
        tk.Label(self, text="INGAME SECONDS PER SCREENSHOT").grid(row=1, column=0, padx= 5)
        var_ts = tk.IntVar(self)
        var_ts.set(Utils.ingame_seconds_per_screenshot)
        TS = tk.Spinbox(self, from_=1, to=5000, textvariable= var_ts)
        TS.grid(row=1, column=1, padx= 5)
        var_ns = tk.IntVar(self)
        var_ns.set(Utils. number_of_screenshot)
        tk.Label(self, text="Number Of Screenshots").grid(row=2, column=0, padx=5)
        NS = tk.Spinbox(self, from_=1, to=200,textvariable=var_ns)
        NS.grid(row=2, column=1, padx=5, pady=70)

        img = Image.fromarray(Utils.ant_screenshot())
        Screenshot = ImageTk.PhotoImage(image = img)
        Screenshot = Screenshot._PhotoImage__photo.subsample(2, 2)
        Screen = tk.Button(self, image = Screenshot, command =lambda: [Utils.find_coords(),
                                                                       master.switch_frame(Home)])
        Screen.image = Screenshot
        Screen.grid(row = 0, column=2, padx=20, pady=20,rowspan=4)

        avvio = tk.Button(self, text="START",
                  command=lambda: [
                                    Utils.set_Time_Screen(var_ts.get()),
                                    Utils.set_Number_Screenshot(var_ns.get()),
                                    Utils.screenshot(),
                                    Utils.organize_images(),
                                    master.switch_frame(Elaborazione)
                                    ])
        avvio.grid(row=5,columnspan=10, pady=10, sticky=tk.NSEW)

class Elaborazione(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        master.title("HEATMAP")
        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff", width=700, height=700)
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.settings = tk.Frame(self, background="#ffffff")
        self.canvas.grid_rowconfigure(0, weight=1)
        self.canvas.grid_columnconfigure(0, weight=1)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.canvas.grid(row=0,column=0, sticky=tk.NSEW)
        self.vsb.grid(row=0, column=1, sticky=tk.NSEW)
        self.settings.grid(row=0, column = 2, sticky=tk.NSEW)



        self.canvas.create_window((4, 4), window=self.frame, anchor="nw",
                                  tags="self.frame")
        self.frame.bind("<Configure>", self.onFrameConfigure)
        self.populate()

        tk.Button(self, text="CREATE HEATMAP", command=lambda:[
                                                                Utils.set_Pixel_Intensity(var_pix_int.get()),
                                                                Utils.set_Around_Pixel_Intensity(var_pix_int_vic.get()),
                                                                Utils.readconfig(),
                                                                Utils.generazione_heatmap()
                                                               ]).grid(row=1, columnspan=3, sticky=tk.NSEW)

        var_pix_int = tk.IntVar(self)
        var_pix_int.set(Utils.intensita_pixel)
        tk.Button(self.settings, text="HOMEPAGE", command=lambda:master.switch_frame(Home), background="#ffffff").grid(row=0, column=0, pady=5)

        tk.Label(self.settings, text =  "PIXEL INTENSITY", background="#ffffff").grid(row=1, column=0, sticky= tk.NSEW)
        PI = tk.Spinbox(self.settings, from_=1, to=5, textvariable=var_pix_int, background="#ffffff")
        PI.grid(row=2, column=0, padx=5, sticky= tk.NSEW)
        var_pix_int_vic = tk.IntVar(self)
        var_pix_int_vic.set(Utils.intensita_p_vicini)
        tk.Label(self.settings, text="RANGE OF PIXEL COLOURATION", background="#ffffff").grid(row=3, column=0, sticky= tk.NSEW)
        PI_V = tk.Spinbox(self.settings, from_=0, to=5, textvariable=var_pix_int_vic, background="#ffffff")
        PI_V.grid(row=4, column=0, padx=5, sticky= tk.NSEW)
        tk.Button(self.settings, text= "RELOAD SCREEN", command=self.reload, background="#ffffff").grid(row=5, column=0, sticky=tk.NSEW)

    def populate(self):
            btn_img = []
            btn_remove = []
            btn_rem_disk =[]
            images = glob.glob('elab_movimenti/*.png')
            ants = []
            padx = 10
            pady=10
            if(len(images) == 0):
                self.no_screenshot()

            for i in range( len(images)):
                ants.append(tk.PhotoImage(file=images[i]))
                ants[i] = ants[i].subsample(3,3)
                btn_img.append(tk.Button(self.frame, text=images[i], image=ants[i],
                                         compound=tk.TOP, command= lambda  c=i: self.getImage(c)))
                btn_remove.append(tk.Button(self.frame, text = "REMOVE FROM QUEUE", command = lambda c=i : [
                                                                                                        os.remove(images[c]),
                                                                                                        self.refresh()
                                                                                                        ]))
                btn_rem_disk.append(tk.Button(self.frame, text = "REMOVE FROM DISK", command = lambda c=i : [
                                                                                                        os.remove(images[c]),
                                                                                                        os.remove(images[c].replace("elab_","")),
                                                                                                        self.refresh()
                                                                                                        ]))
                btn_img[i].image = ants[i]
                btn_img[i].grid(row = i, column=0, sticky=tk.NS, padx = padx, pady = pady)
                btn_remove[i].grid(row = i, column = 1, sticky=tk.NS, padx = padx, pady = pady)
                btn_rem_disk[i].grid(row = i, column = 2, sticky=tk.NS, padx = padx, pady = pady)

    def onFrameConfigure(self, event):
            '''Reset the scroll region to encompass the inner frame'''
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def getImage(self,i):
        images = glob.glob('elab_movimenti/*.png')
        image = cv2.imread(images[i])
        cv2.imshow(images[i], image)
        # add wait key. window waits until user presses a key
        cv2.waitKey(0)

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
        tk.Label(top, text= """HEY BRO, SEEMS LIKE YOU HAVEN'T GOT SCREENSHOTS YET.
    WHERE DO YOU WANNA GET BACK?""").grid(row=0, columnspan=2)
        tk.Button(top, text= "HOMEPAGE", command=lambda: [self.master.switch_frame(Home), top.destroy()]).grid(row=1, column=0)
        tk.Button(top, text= "SCREENSHOT", command=lambda: [self.master.switch_frame(Screenshot), top.destroy()]).grid(row=1, column=1)






def main():
    Utils.readconfig()
    app = GUI_APP()
    app.configure(background='white')
    app.resizable(False, False)
    app.mainloop()