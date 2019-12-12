from features import *

rgb_img = io.imread("images/trial.png")
print("read")
cr_img = rgb2cr(rgb_img)
print("cr_img")
segmented = segment(cr_img)
print("segmented")

dist_trans, img_centroid,centroid = refpoint(segmented)
#show_images([segmented])
dists = descriptor(segmented, [3195, 2000], 180)
#center=getCenter(segmented,rgb_img)

#print("refpoint: ",centroid," center: ",center)


#show_images([rgb_img, cr_img, segmented, dist_trans, img_centroid])