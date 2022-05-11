import cv2
import numpy as np
import GUI
import os
np.set_printoptions(threshold=np.inf)

def programma():
    if not os.path.exists('movimenti'):
        os.mkdir('movimenti')
    if not os.path.exists('elab_movimenti'):
        os.mkdir('elab_movimenti')
    if not os.path.exists('HEATMAPS'):
        os.mkdir('HEATMAPS')
    GUI.main()


if __name__ == '__main__':
    programma()
    cv2.destroyAllWindows()

