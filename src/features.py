from commonfunctions import *
from preprocessing import *
import numpy as np
import cv2
import skimage.io as io
from scipy import ndimage
from numpy import unravel_index
import math


def refpoint(img):
    dist_trans = ndimage.distance_transform_edt(img)
    centroid = unravel_index(dist_trans.argmax(), dist_trans.shape)
    x = centroid[0]
    y = centroid[1]
    img_centroid = np.copy(img)
    cv2.circle(img_centroid, (x, y), 80, (0, 0, 0), -1)
    return dist_trans, img_centroid, centroid


def descriptor(image, center, descriptor):
    step = int(360/descriptor)
    dists = []
    for i in range(2, 360, step):
        if i == 90:
            y = np.arange(center[0]+1, np.shape[0])
            x = np.full(len(y), center[1])
        elif i == 270:
            y = np.arange(center[0]-1, -1, -1)
            x = np.full(len(y), center[1])
        else:
            m = math.tan((i * math.pi) / 180)
            if 0 <= i < 90 or 270 < i <= 360:
                x = np.arange(center[1]+1, image.shape[1])
            else:
                x = np.arange(center[1]-1, -1, -1)
            y = np.array(np.round(m * (x - center[1]) + center[0])).astype(int)
        points=np.array([y,x]).T
        point = [i for i in points if image[i[0],i[1]] == 0][0]
        dist = math.sqrt(pow(point[0]-center[0], 2)+pow(point[1]-center[1], 2))
        dists.append(dist)
    mindist = min(dists)
    dists /= mindist
    return dists











