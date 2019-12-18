from commonfunctions import *
from preprocessing import *
import numpy as np
import cv2
import skimage.io as io
from scipy import ndimage
from numpy import unravel_index
import math
import xlwt
from xlwt import Workbook


def refpoint(img):
    dist_trans = ndimage.distance_transform_edt(img)
    centroid = unravel_index(dist_trans.argmax(), dist_trans.shape)
    x = centroid[0]
    y = centroid[1]
    img_centroid = np.copy(img)
    cv2.circle(img_centroid, (x, y), 80, (0, 0, 0), -1)
    return dist_trans, img_centroid,centroid


def descriptor(image, center, descriptor):
    step = int(360/descriptor)
    dists = []
    for i in range(0, 360, step):
        if i == 90:
            y = np.arange(center[0]+1, image.shape[0])
            x = np.full(len(y), center[1])
        elif i == 270:
            y = np.arange(center[0]-1, -1, -1)
            x = np.full(len(y), center[1])
        else:
            m = math.tan((i * math.pi) / 180)
            if 0 <= i < 90 or 270 < i <= 360:
                x = np.arange(center[1]+1, image.shape[1])
                flag=0
            else:
                x = np.arange(center[1]-1, -1, -1)
                flag=1
            y = np.array(np.round(m * (x - center[1]) + center[0])).astype(int)
        points=np.array([y,x]).T
        point = [j for j in points if center[0] <= j[0] < image.shape[0] and image[j[0], j[1]] ==0]
        #print(i)
        if len(point) == 0:
            if (flag == 0 and m > 0) or (flag == 1 and m < 0):
                point = max([k for k in points if k[0] < image.shape[0]], key=lambda x: x[0])
            else:
                point = min([k for k in points if k[0] > 0],key=lambda x: x[0])
            y1 = y[y == point[0]]
            x1 = x[y == point[0]]
            if m > 0:
                y1 = y1[x1 == max(x1)]
                x1 = x1[x1 == max(x1)]
            else:
                y1 = y1[x1 == min(x1)]
                x1 = x1[x1 == min(x1)]
            point = [y1, x1]
        else:
            point = point[0]
        dist = math.sqrt(pow(point[0]-center[0], 2)+pow(point[1]-center[1], 2))
        dists.append(dist)
    mindist = min(dists)
    dists=np.array(dists)
    dists /= mindist
    return dists


def writeFeatures(dists,labels):
    wb = Workbook()

    # add_sheet is used to create sheet.










