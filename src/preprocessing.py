from src.commonfunctions import *
import numpy as np
import skimage.io as io


def rgb2ycbcr(rgb_img):
    cr_img = np.zeros((rgb_img.shape[0], rgb_img.shape[1]))
    r = rgb_img[:, :, 0]
    g = rgb_img[:, :, 1]
    b = rgb_img[:, :, 2]
    cr_img = 0.5*r - 0.418688*g - 0.081312*b

    return cr_img


def segment(cr_img):
    segmented = np.copy(cr_img)
    segmented[segmented[:, :] < 0] = 0
    segmented[segmented[:, :] > 0] = 1

    return segmented


