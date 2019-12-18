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
    original=image.shape[1]
    starth, endh, centerh = getBorders(image,0)
    startv, endv, centerv = getBorders(image,1)
    image=image[startv:endv+1, starth:endh+1]
    #image = image[startv:endv + 1, :]
    return image, centerh, centerv,original


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
    hand[hand<255]=0
    HP = sum(hand[hand.shape[0]-1,:])
    start = int((3/4)*(hand.shape[0]-1))
    #start=hand.shape[1]-1
    cropPoint = start
    for i in range(start,-1,-1):
        curr = sum(hand[i,:])
        if curr > HP:
            cropPoint = i
            break
        HP = curr
    # print(HP)
    # print(curr)
    # print(cropPoint)
    # print(hand.shape[0]-4)
    hand = hand[0:cropPoint+3, :]
    hand[hand.shape[0]-1, :] = 0
    hand[0, :] = 0
    hand[:, hand.shape[1] - 1] = 0
    hand[:, 0] = 0
    return hand


def extractTip(img):
    img1 = np.array(img)
    index = np.where(img1 == 255)[0][0]
    tip = index + 100
    rows = img1.shape[0] - tip
    cols = img1.shape[1]
    sub = np.zeros((rows, cols))
    img1[tip:][:] = sub
    return img1
def ZJF(image):
    start=0
    end=0
    start1=0
    end1=0
    HP=[]
    hp=0
    VP=[]
    vp=0



    for i in range (image.shape[0]):
        for j in range(image.shape[1]):
            hp+=image[i][j]
        HP.append(hp)
    for i in range (image.shape[1]):
        for j in range(image.shape[0]):
            hp+=image[j][i]
        VP.append(vp)
    for i in range(image.shape[1]):
        if image[HP==max(HP)][j]==1:
            start1=i
            break
    for i in range(image.shape[1]-1,0,-1):
        if image[HP==max(HP)][j]==1:
            end1=i
            break
    for i in range (image.shape[0]):
        if image[i][np.floor(image.shape[1]/2)]==1:
            start=i
            break
    for i in range (image.shape[0]-1,0,-1):
        if image[i][np.floor(image.shape[1]/2)]==1:
            end=i
            break
    hight=end-start
    width=max(HP)
    HP=np.asarry(HP)
    VP = np.asarry(VP)
    HP=HP/width
    VP=VP/hight
    HP1=HP[start:end,start1:end1]
    VP1=VP[start:end,start1:end1]
    return HP1,VP1
