from src.commonfunctions import *
import numpy as np
import skimage.io as io
import cv2


def skewCorrection(image):
    #thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated


def rgb2ycbcr(rgb_img):
    img = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2YCrCb)
    y = img[:, :, 0]
    cr = img[:, :, 1]
    cb = img[:, :, 2]
    y1 = y.copy()
    cr1 = cr.copy()
    cb1 = cb.copy()

    y[y1 > 80] = 0
    y[y1 <= 80] = 255

    cr[cr1 >= 133] = 255
    cr[cr1 <= 173] = 255
    cr[cr1 < 133] = 0
    cr[cr1 > 173] = 0

    cb[cb1 <= 120] = 255
    cb[cb1 >= 80] = 255
    cb[cb1 > 120] = 0
    cb[cb1 < 80] = 0
    return y, cb, cr


def hand(image):
    y, cr, cb = rgb2ycbcr(image)
    hand = (cr+cb)
    hand[hand > 0] = 255
    hand = skewCorrection(hand)
    kernel = np.ones((3, 3), np.uint8)
    hand = cv2.morphologyEx(hand, cv2.MORPH_CLOSE, kernel, iterations=3)
    return hand


def getBorders(image, type):
    VPs = []
    if type==0:
        stop=image.shape[1]
    else:
        stop=image.shape[0]

    for i in range(stop):
        if type == 0:
            VPs.append(sum(image[:, i]))
        else:
            VPs.append(sum(image[i, :]))

    i = 0
    while i < len(VPs) and VPs[i] == 0:
        i += 1
    start = i
    i = len(VPs)-1
    while i >= 0 and VPs[i] == 0:
        i -= 1
    end = i
    center = (start+end)/2
    return start, end, center


def cropPicture(image):
    starth, endh, centerh = getBorders(image,0)
    startv, endv, centerv = getBorders(image,1)
    image=image[startv:endv, starth:endh]
    return image, centerh, centerv


def transform(image,index):
    state = 0
    trans = 0
    for i in range(image.shape[0]):
        if state == 0 and image[i][index]>0:
            trans += 1
            state=1
        elif state==1 and  image[i][index]==0:
            trans+=1
            state=0
            if trans==2:
                return True,i
    return False,None


def extractFist(hand):

    HP = sum(hand[hand.shape[0]-1,:])
    for i in range(hand.shape[1]-2,-1,-1):
        curr = sum(hand[i,:])
        if curr > HP:
            cropPoint = i
            break
        HP = curr
    hand = hand[0:cropPoint+1]
    return hand


def extractTip(img):
    img1 = np.array(img)
    rows = img1.shape[0]-50
    cols = img1.shape[1]
    sub = np.zeros((rows, cols))
    img1[50:][:] = sub
    return img1


img = io.imread("../images/L.jpg")
img = hand(img)
img, centerh, centerv = cropPicture(img)
img = extractFist(img)
img = extractTip(img)
show_images([img])

