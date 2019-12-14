from features import *
import os


#rgb_img = io.imread("../images/ASL/A/A1.jpg")
# hands=[]
# dirs=[r'../images/A',r'../images/B',r'../images/C',r'../images/D',r'../images/O',r'../images/X,',r'../images/Y']
# for i in range(len(dirs)):
#     fnames = os.listdir(dirs[i])
#     for fn in fnames:
#         path = os.path.join(r'../images/A', fn)
#         img=io.imread(path)
#         hand=hand(img)
#         hands.append(hand)

img=io.imread("../images/A/A (21).jpg")
img = hand(img)
img, centerh, centerv=cropPicture(img)
img = extractFist(img)
show_images([img])

# dist_trans, img_centroid,centroid = refpoint(segmented)

# dists = descriptor(segmented, [3195, 2000], 180)
# center=getCenter(segmented,rgb_img)
# print("refpoint: ",centroid," center: ",center)
# show_images([rgb_img, cr_img, segmented, dist_trans, img_centroid])
