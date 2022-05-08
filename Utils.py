import time
from PIL import ImageGrab
import cv2
import numpy as np
import configparser
import glob
from datetime import datetime
import os
import shutil
import mouse


intensita_pixel=3
intensita_p_vicini = 1
ingame_seconds_per_screenshot = 40
number_of_screenshot = 15

x_iniziale = 0
y_iniziale = 0
x_finale = 1000
y_finale = 500
x_bar = 0
y_bar = 0

lower = np.array([0,0,120])
upper = np.array([40,170,255])
CONF_FILE = "config.ini"
config = configparser.ConfigParser()


def screenshot():
    read_bar()
    readconfig()
    x = 0
    print(number_of_screenshot)
    while(x<number_of_screenshot):
        print(x)
        now = datetime.now()  # current date and time
        file_name = str(now.strftime("%m-%d-%Y %H-%M-%S"))
        print(file_name)
        for s in range(ingame_seconds_per_screenshot):
            mouse.move(x_bar, y_bar)
            mouse.click('left')
            time.sleep(0.01)

        time.sleep(1)
        img = ImageGrab.grab(bbox=(x_iniziale, y_iniziale, x_finale, y_finale))  # x, y, w, h.
        img_np = np.array(img)
        RGB_img = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
        cv2.imwrite("movimenti/"+file_name+".png", RGB_img)
        x+=1
    path = os.path.abspath("movimenti/")
    os.startfile(path)



def ant_screenshot():
    readconfig()
    img = ImageGrab.grab(bbox=(x_iniziale, y_iniziale, x_finale, y_finale))  # x, y, w, h.
    img_np = np.array(img)
    RGB_img = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
    return RGB_img

def find_coords():

    def click_event(event, x, y, flags, params):
        global x_finale
        global x_iniziale
        global y_finale
        global y_iniziale


        # checking for left mouse clicks

        if event == cv2.EVENT_LBUTTONDOWN:
            # displaying the coordinates
            # on the Shell

            x_iniziale =x
            y_iniziale = y




        # checking for right mouse clicks
        if event == cv2.EVENT_RBUTTONDOWN:
            # displaying the coordinates
            # on the Shell
            x_finale = x
            y_finale = y
            cv2.destroyWindow("image")
            save_config()

    img = ImageGrab.grab(bbox=(0, 0, 1920, 1080))  # x, y, w, h.
    img_np = np.array(img)
    RGB_img = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
    cv2.imshow('image', RGB_img)
    cv2.setMouseCallback('image', click_event)

def read_bar():
    def click_event(event, x, y, flags, params):
        global x_bar
        global y_bar


        # checking for left mouse clicks

        if event == cv2.EVENT_LBUTTONDOWN:
            # displaying the coordinates
            # on the Shell
            cv2.destroyWindow("image")
            x_bar = x
            y_bar = y
            save_config()


    img = ImageGrab.grab(bbox=(0, 0, 1920, 1080))  # x, y, w, h.
    img_np = np.array(img)
    RGB_img = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
    cv2.putText(img=RGB_img, text='CLICK THE END OF THE TIME BAR', org=(100, 100), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=3,
                color=(0, 255, 0))
    cv2.imshow('image', RGB_img)

    cv2.setMouseCallback('image', click_event)
    cv2.waitKey(0)


def save_config():
    config['DEFAULT'] = {
        'intensita_pixel': intensita_pixel,
        'intensita_pixel_vicini': intensita_p_vicini,
        'number_of_screenshot': number_of_screenshot,
        'ingame_seconds_per_screenshot' : ingame_seconds_per_screenshot,
        'x_iniziale': x_iniziale,
        'y_iniziale': y_iniziale,
        'x_finale': x_finale,
        'y_finale': y_finale,
        'x_bar' : x_bar,
        'y_bar' : y_bar
    }
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def readconfig():
        global x_iniziale, x_finale, y_finale, y_iniziale, intensita_pixel, intensita_p_vicini, ingame_seconds_per_screenshot, number_of_screenshot, x_bar, y_bar
        if glob.glob(CONF_FILE):
            config.read(CONF_FILE)
            intensita_pixel = int (config['DEFAULT']['intensita_pixel'])
            intensita_p_vicini = int (config['DEFAULT']['intensita_pixel_vicini'])
            ingame_seconds_per_screenshot = int(config['DEFAULT']['ingame_seconds_per_screenshot'])
            number_of_screenshot = int(config['DEFAULT']['number_of_screenshot'])
            x_iniziale = int(config['DEFAULT']['x_iniziale'])
            y_iniziale = int(config['DEFAULT']['y_iniziale'])
            x_finale = int(config['DEFAULT']['x_finale'])
            y_finale = int(config['DEFAULT']['y_finale'])
            x_bar = int(config['DEFAULT']['x_bar'])
            y_bar = int(config['DEFAULT']['y_bar'])
        else:
            print("NO CONFIG FILE, USING THE DEFAULT ONES")

def lettura_immagini(heatmap):

    for movimento in glob.glob('elab_movimenti/*.png'):
        image = cv2.imread(movimento)
        mask = cv2.inRange(image, lower, upper)
        coord = cv2.findNonZero(mask)
        intensita(heatmap, coord)

def intensita(array, coord):
    for c in coord:
        x = c[0][0]
        y= c[0][1]

        array[x, y] += intensita_pixel
        try:
            for s in range(20):
                array[x+s, y] += intensita_p_vicini
                array[x, y+s] += intensita_p_vicini
                array[x-s, y] += intensita_p_vicini
                array[x, y-s] += intensita_p_vicini
        except:
            pass

def generazione_heatmap():
    heatmap = np.zeros((x_finale - x_iniziale, y_finale - y_iniziale))
    lettura_immagini(heatmap)
    print('Lettura eseguita')
    heatmapshow = None
    heatmapshow=heatmap*20
    heatmapshow = cv2.normalize(heatmap, heatmapshow, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    heatmapshow = cv2.applyColorMap(heatmapshow, cv2.COLORMAP_INFERNO)

    print(heatmapshow.shape)
    x_campo=  x_finale - x_iniziale
    y_campo =  y_finale - y_iniziale
    Campo = cv2.imread("src//Campo.png")
    Campo = cv2.resize(Campo, ( y_campo, x_campo))
    heatmapshow = cv2.addWeighted(Campo, 1, heatmapshow, 2, 0)
    cv2.imshow('Heatmap', heatmapshow)
    cv2.waitKey(0)

def set_Time_Number_Screen(ts,ns):
    global ingame_seconds_per_screenshot, number_of_screenshot
    ingame_seconds_per_screenshot = ts
    number_of_screenshot = ns
    save_config()

def organize_images():
    source_folder = "movimenti"
    path = "elab_movimenti"
    shutil.copytree(source_folder, path,dirs_exist_ok=True)