# import cv2
# def getCenter(segmented,real):
#     img=segmented.copy()
#     #img = img.astype(np.uint8) * 255
#     #img = np.array(img, dtype='uint8')*255
#     img=np.array(img,dtype=np.double)
#     #img=img[500:img.shape[0]-600,500:img.shape[0]-600]
#     #newC = np.array(measure.find_contours(img,0.5)).astype(int)
#     #cv2.drawContours(real, [newC[0]], -1, (0, 255, 0), -1)
#     cv2.imshow('Image_Circle', real)
#     cv2.waitKey(0)
#     # contours = np.where(img > 0)
#     # contours=np.array([contours[1],contours[0]])
#     # contours = contours.T
#     contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#     cv2.drawContours(img, contours[1], -1, (0, 0, 255), -1)
#     M = cv2.moments(contours)
#     cX = int(M["m10"] / M["m00"])
#     cY = int(M["m01"] / M["m00"])
#     return cX, cY
#
#


# contours, hierarchy = cv2.findContours(hand, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# R=np.copy(hand.T)
# G=np.zeros((hand.shape[1],hand.shape[0]))
# B=np.zeros((hand.shape[1],hand.shape[0]))
# img = (np.array([R,G,B]).T).astype(int)
# cv2.drawContours(img, [contours[2]], -1, (0, 255, 0), 5)




# from preprocessing import *
#
# img = io.imread("../images/trial.png")
# cr_img = rgb2ycbcr(img)
# osegmented = segment(cr_img)
# segmented = np.array(osegmented, dtype='uint8')*255
# #segmented = cv2.copyMakeBorder(segmented, 1, 1, 1, 1, cv2.BORDER_CONSTANT)
# contours, hierarchy = cv2.findContours(segmented, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#
# R = osegmented
# G = osegmented*0
# B = osegmented*0
# newImg=np.array([R,G,B])
#
# #cv2.drawContours(newImg, contours, -1, (0, 255, 0), 3)
# #cv2.imshow('Image_Circle', newImg)
# #cv2.waitKey(0)
# show_images([newImg])
#
#
#
# # import numpy as np
# # x=np.arange(1,5)
# # print(x)


from skimage.viewer import ImageViewer

import cv2
from commonfunctions import *

img = io.imread("../images/A.PNG")
img = cv2.cvtColor(img, cv2.COLOR_RGB2YCrCb)
y=img[:,:,0]
cr=img[:,:,1]
cb=img[:,:,2]
show_images([y,cr,cb])

#y[y>80]=255

# for i in range(cb.shape[0]):
#     for j in range(cb.shape[1]):
#         if 80<=cb[i][j]<=120:
#             cb[i][j]=255
#         else:
#             cb[i][j]=0

cr[cr>133]=255
cr[cr<173]=255

cb[cb<120]=255

cb[cb>80]=255
show_images([y,cr,cb])

#show_images([cb])
