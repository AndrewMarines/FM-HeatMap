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
import ctypes
import GUI
from multiprocessing import Process
user32 = ctypes.windll.user32

intensita_pixel = 3
intensita_p_vicini = 1
ingame_seconds_per_screenshot = 40
number_of_screenshot = 15
x_iniziale = 0
y_iniziale = 0
x_finale = 400
y_finale = 400
x_bar = 0
y_bar = 0

lower = np.array([0, 0, 120])
upper = np.array([40, 170, 255])
CONF_FILE = "config.ini"
config = configparser.ConfigParser()


def get_time():
    now = datetime.now()  # current date and time
    formatted_time = str(now.strftime("%m-%d-%Y %H-%M-%S"))
    return formatted_time


def screenshot(master, folder):
    read_bar(master)
    readconfig()
    x = 0
    if not os.path.exists('movimenti/' + folder):
        os.mkdir('movimenti/' + folder)
    while (x < number_of_screenshot):
        file_name = get_time()
        for s in range(ingame_seconds_per_screenshot):
            mouse.move(x_bar, y_bar)
            mouse.click('left')
            time.sleep(0.01)

        time.sleep(1)
        img = ImageGrab.grab(bbox=(x_iniziale, y_iniziale, x_finale, y_finale))  # x, y, w, h.
        img_np = np.array(img)
        rgb_img = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
        cv2.imwrite("movimenti/" + folder + '/' + file_name + ".png", rgb_img)
        print(file_name)
        x += 1
    path = os.path.abspath("movimenti/")
    os.startfile(path)


def ant_screenshot():
    readconfig()
    img = ImageGrab.grab(bbox=(x_iniziale, y_iniziale, x_finale, y_finale))  # x, y, w, h.
    img_np = np.array(img)
    RGB_img = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
    return RGB_img


def find_coords(master):
    def click_event(event, x, y, flags, params):
        global x_finale
        global x_iniziale
        global y_finale
        global y_iniziale

        # checking for left mouse clicks

        if event == cv2.EVENT_LBUTTONDOWN:
            # displaying the coordinates
            # on the Shell

            x_iniziale = x
            y_iniziale = y

        # checking for right mouse clicks
        if event == cv2.EVENT_RBUTTONDOWN:
            # displaying the coordinates
            # on the Shell
            x_finale = x
            y_finale = y
            save_config()
            cv2.destroyWindow("image")
            master.state('normal')

    img = ImageGrab.grab(bbox=(0, 0, user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)))  # x, y, w, h.
    img_np = np.array(img)
    rgb_img = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
    cv2.imshow('image', rgb_img)
    cv2.setMouseCallback('image', click_event)


def read_bar(master):
    def click_event(event, x, y, flags, params):
        global x_bar
        global y_bar

        # checking for left mouse clicks

        if event == cv2.EVENT_LBUTTONDOWN:
            # displaying the coordinates
            # on the Shell
            cv2.destroyWindow("image")
            x_bar = int(x + user32.GetSystemMetrics(0) / 2)
            print(x)
            print(x_bar)
            y_bar = int(y + (user32.GetSystemMetrics(1) * 10) / 100)
            save_config()

    img = ImageGrab.grab(bbox=(
        int(user32.GetSystemMetrics(0) / 2), int(0 + (user32.GetSystemMetrics(1) * 10) / 100),
        user32.GetSystemMetrics(0),
        int(user32.GetSystemMetrics(1) - (user32.GetSystemMetrics(1) * 10) / 100)))  # x, y, w, h.

    master.iconify()
    img_np = np.array(img)
    rgb_img = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
    cv2.imshow('image', rgb_img)

    cv2.setMouseCallback('image', click_event)
    cv2.waitKey(0)


def save_config():
    config['DEFAULT'] = {
        'intensita_pixel': intensita_pixel,
        'intensita_pixel_vicini': intensita_p_vicini,
        'number_of_screenshot': number_of_screenshot,
        'ingame_seconds_per_screenshot': ingame_seconds_per_screenshot,
        'x_iniziale': x_iniziale,
        'y_iniziale': y_iniziale,
        'x_finale': x_finale,
        'y_finale': y_finale,
        'x_bar': x_bar,
        'y_bar': y_bar
    }
    with open('config.ini', 'w') as configfile:
        config.write(configfile)


def readconfig():
    global x_iniziale, x_finale, y_finale, y_iniziale, intensita_pixel, intensita_p_vicini, ingame_seconds_per_screenshot, number_of_screenshot, x_bar, y_bar
    if glob.glob(CONF_FILE):
        config.read(CONF_FILE)
        intensita_pixel = int(config['DEFAULT']['intensita_pixel'])
        intensita_p_vicini = int(config['DEFAULT']['intensita_pixel_vicini'])
        ingame_seconds_per_screenshot = int(config['DEFAULT']['ingame_seconds_per_screenshot'])
        number_of_screenshot = int(config['DEFAULT']['number_of_screenshot'])
        x_iniziale = int(config['DEFAULT']['x_iniziale'])
        y_iniziale = int(config['DEFAULT']['y_iniziale'])
        x_finale = int(config['DEFAULT']['x_finale'])
        y_finale = int(config['DEFAULT']['y_finale'])
        x_bar = int(config['DEFAULT']['x_bar'])
        y_bar = int(config['DEFAULT']['y_bar'])
    else:
        print("NO CONFIG FILE, CREATING A DEFAULT ONE")
        save_config()


def lettura_immagini(heatmap, height, width):


    for movimento in glob.glob( "elab_movimenti/**/*.png", recursive=True):
        print(movimento)
        image = cv2.imread(movimento)
        image = cv2.resize(image, (width, height))
        mask = cv2.inRange(image, lower, upper)
        coord = cv2.findNonZero(mask)
        intensita(heatmap, coord)




def intensita(array, coord):
    for c in coord:

        y = c[0][0]
        x = c[0][1]

        array[x, y] += intensita_pixel
        try:
            for s in range(20):
                array[x + s, y] += intensita_p_vicini
                array[x, y + s] += intensita_p_vicini
                array[x - s, y] += intensita_p_vicini
                array[x, y - s] += intensita_p_vicini
        except:
            pass


def generazione_heatmap():
    first_image = glob.glob("elab_movimenti/**/*.png", recursive=True)[0]
    first_image = cv2.imread(first_image)
    height = first_image.shape[0]
    width = first_image.shape[1]
    heatmap = np.zeros((height, width))
    lettura_immagini(heatmap, height, width)
    heatmapshow = None
    heatmapshow = heatmap * 20
    heatmapshow = cv2.normalize(heatmap, heatmapshow, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    heatmapshow = cv2.applyColorMap(heatmapshow, cv2.COLORMAP_INFERNO)

    Campo = cv2.imread("src//Campo.png")
    Campo = cv2.resize(Campo, (width, height))
    heatmapshow = cv2.addWeighted(Campo, 1, heatmapshow, 2, 0)
    now = datetime.now()  # current date and time
    file_name = str(now.strftime("%m-%d-%Y %H-%M-%S"))
    print("GENERATED HEATMAP")
    return heatmapshow


def set_Time_Screen(ts):
    global ingame_seconds_per_screenshot
    ingame_seconds_per_screenshot = ts
    save_config()


def set_Number_Screenshot(ns):
    global number_of_screenshot
    number_of_screenshot = ns
    save_config()


def set_Pixel_Intensity(PI):
    global intensita_pixel
    intensita_pixel = PI
    save_config()


def set_Around_Pixel_Intensity(A_P_I):
    global intensita_p_vicini
    intensita_p_vicini = A_P_I
    save_config()


def organize_images():
    source_folder = "movimenti"
    path = "elab_movimenti"
    shutil.rmtree(path)
    shutil.copytree(source_folder, path, dirs_exist_ok=True)
    text_files = glob.glob(source_folder + "/**/*.png", recursive=True)


def rotate_image(img, path):
    rotated_image = np.rot90(img)
    rotated_image = np.rot90(rotated_image)
    cv2.imwrite(path, rotated_image)
