import cv2
import numpy as np
from resize_image import image_resize


# defining minimal and maximal radius, specified to the coins.jpg
min_r = 10
max_r = 50

img = cv2.imread('input_image/6.jpg',0)
img = image_resize(img, width =  250)
orig = img
img = cv2.medianBlur(img,5)
cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

# v1
# circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 40, param1=50, param2=30, minRadius=min_r, maxRadius=max_r)
# el bueno
circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 40, param1=40, param2=30, minRadius=min_r, maxRadius=max_r)
# v2
# circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 40, param1=50, param2=20, minRadius=min_r, maxRadius=max_r)
circles = np.uint16(np.around(circles))

# ensure at least some circles were found
if circles is not None:
    # loop over the (x, y) coordinates and radius of the circles
    for i in circles[0,:]:
        # draw the outer circle
        cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),1)
        # draw the center of the circle
        cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
        cv2.putText(cimg,'{}'.format(i[2]),(i[0],i[1]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0))
        print('radio:{}'.format(i[2]))
    # show result
    cv2.imshow('Detected circles',cimg)
    cv2.imshow('Original',orig)
    cv2.waitKey(0)
    cv2.destroyAllWindows()






