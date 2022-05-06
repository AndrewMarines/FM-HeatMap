import cv2
import numpy as np
import glob
from PIL import ImageGrab
import time
import matplotlib.pyplot as plt
np.set_printoptions(threshold=np.inf)


intensita_pixel=3
intensita_p_vicini = 1
lower = np.array([0,0,120])  # BGR-code of your lowest red
upper = np.array([40,170,255])   # BGR-code of your highest red

def generazione_heatmap(img):
    heatmapshow = None
    img=img*20
    heatmapshow = cv2.normalize(img, heatmapshow, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    heatmapshow = cv2.applyColorMap(heatmapshow, cv2.COLORMAP_INFERNO)
    Campo = cv2.imread("Campo.png")
    Campo = cv2.resize(Campo, (474, 735))

    heatmapshow = cv2.addWeighted(Campo, 1, heatmapshow, 2, 0)

    return heatmapshow

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

def screenshot():
    x = 0
    while(x<28):
        img = ImageGrab.grab(bbox=(900, 145, 1635, 619))  # x, y, w, h.
        img_np = np.array(img)
        RGB_img = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
        cv2.imwrite("movimenti/"+str(x)+".png", RGB_img)
        x+=1
        time.sleep(20)
    print("finito")

def programma():
    screenshot()
    heatmap = np.zeros((735, 474))

    for movimento in glob.glob('movimenti/*.png'):

        image = cv2.imread(movimento)
        mask = cv2.inRange(image, lower, upper)
        coord = cv2.findNonZero(mask)
        intensita(heatmap, coord)




    #combined = cv2.addWeighted(mask, 0.9, mask2, 0.9, 0)
    # get all non zero values

    #cv2.imshow("Heatmap", generazione_heatmap(combined))
    #cv2.waitKey(0)
    #cv2.imwrite('color_img.jpg', heatmap)
    cv2.imshow('Color image', generazione_heatmap(heatmap))
    cv2.waitKey(0)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    programma()
    cv2.destroyAllWindows()

