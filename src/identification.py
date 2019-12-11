from src.commonfunctions import *
from preprocessing import *
import numpy as np
import cv2
import skimage.io as io
from scipy import ndimage
from numpy import unravel_index

def refpoint(img):
    dist_trans = ndimage.distance_transform_edt(img)
    centroid = unravel_index(dist_trans.argmax(), dist_trans.shape)
    x = centroid[0]
    y = centroid[1]
    img_centroid = np.copy(img)
    cv2.circle(img_centroid, (x, y), 80, (0, 0, 0), -1)
    return dist_trans, img_centroid

# def fingeridentification(img):


rgb_img = io.imread("trial.jpg")
cr_img = rgb2cr(rgb_img)
segmented = segment(cr_img)
dist_trans, img_centroid = refpoint(segmented)

show_images([rgb_img, cr_img, segmented, dist_trans, img_centroid])