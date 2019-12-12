import cv2
def getCenter(segmented,real):
    img=segmented.copy()
    #img = img.astype(np.uint8) * 255
    #img = np.array(img, dtype='uint8')*255
    img=np.array(img,dtype=np.double)
    #img=img[500:img.shape[0]-600,500:img.shape[0]-600]
    #newC = np.array(measure.find_contours(img,0.5)).astype(int)
    #cv2.drawContours(real, [newC[0]], -1, (0, 255, 0), -1)
    cv2.imshow('Image_Circle', real)
    cv2.waitKey(0)
    # contours = np.where(img > 0)
    # contours=np.array([contours[1],contours[0]])
    # contours = contours.T
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contours[1], -1, (0, 0, 255), -1)
    M = cv2.moments(contours)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    return cX, cY


import numpy as np
x=np.arange(1,5)
print(x)