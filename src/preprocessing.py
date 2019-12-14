from src.commonfunctions import *
import numpy as np
import cv2
import skimage.io as io
from scipy.ndimage.morphology import binary_dilation, binary_erosion


def rgb2ycbcr(rgb_img):
    img = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2YCR_CB)
    return img


def segment(img):
    segmented = np.copy(img)
    y = segmented[:, :, 0]
    cr = segmented[:, :, 1]
    cb = segmented[:, :, 2]

    y1 = y.copy()
    cr1 = cr.copy()
    cb1 = cb.copy()

    show_images([y, cr, cb])

    y[y1 <= 163] = 255
    y[y1 < 54] = 0

    # y = binary_dilation(y)
    # y = binary_erosion(y)

    cr[cr1 <= 157] = 255
    cr[cr1 >= 131] = 255
    cr[cr1 > 157] = 0
    cr[cr1 < 131] = 0

    # cr = binary_dilation(cb)
    # cr = binary_erosion(cb)

    cb[cb1 <= 135] = 255
    cb[cb1 >= 110] = 255
    cb[cb1 > 135] = 0
    cb[cb1 < 110] = 0

    # cb = binary_dilation(cr)
    # cb = binary_erosion(cr)

    show_images([y, cr, cb])


img = io.imread('../images/trial.jpg')
img2 = rgb2ycbcr(img)
segment(img2)

