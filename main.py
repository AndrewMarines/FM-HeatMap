import cv2
import numpy as np
import GUI
import os
import multiprocessing
np.set_printoptions(threshold=np.inf)

def programma():
    if not os.path.exists('movimenti'):
        os.mkdir('movimenti')
    if not os.path.exists('elab_movimenti'):
        os.mkdir('elab_movimenti')
    GUI.main()


if __name__ == '__main__':
    multiprocessing.freeze_support()  # support multiprocessing in pyinstaller
    programma()
    cv2.destroyAllWindows()

