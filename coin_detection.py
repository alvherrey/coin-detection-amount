import cv2
import numpy as np
from resize_image import image_resize


# defining minimal and maximal radius, specified to the coins.jpg
min_r = 150
max_r = 300

coins = cv2.imread('input_image/6.jpg',0)
# img = image_resize(img, width =  250)
orig = coins.copy()
# gray = cv2.cvtColor(coins, cv2.COLOR_BGR2GRAY)
img = cv2.medianBlur(coins,9)
cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

# v1
# circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 40, param1=50, param2=30, minRadius=min_r, maxRadius=max_r)
# el bueno
# circles = cv2.HoughCircles(img,  cv2.HOUGH_GRADIENT, 1, 300, param1=30, param2=120, minRadius=min_r, maxRadius=max_r)
# mejor que el bueno
# circles = cv2.HoughCircles(img,  cv2.HOUGH_GRADIENT, 1, 300, param1=20, param2=100, minRadius=min_r, maxRadius=max_r)
circles = cv2.HoughCircles(img,  cv2.HOUGH_GRADIENT, 1, 300, param1=30, param2=100, minRadius=min_r, maxRadius=max_r)

# v2
# circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 40, param1=50, param2=20, minRadius=min_r, maxRadius=max_r)
circles = np.uint16(np.around(circles))

# ensure at least some circles were found
if circles is not None:
    # loop over the (x, y) coordinates and radius of the circles
    for i in circles[0,:]:
        # draw the outer circle
        cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
        cv2.putText(cimg,'{}'.format(i[2]),(i[0],i[1]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0))
        print('radio:{}'.format(i[2]))
    # show result
    # cv2.imshow('Detected circles',cimg)
    # cv2.imshow('Original',orig)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    cv2.imwrite("output_image/coin_amount/resultado.jpg", cimg)
    cv2.imwrite("output_image/coin_amount/original.jpg", orig)






