import cv2
import numpy as np

# load the image, clone it for output, and then convert it to grayscale
coins = cv2.imread('input_image/coins.jpg')
output = coins.copy()
gray = cv2.cvtColor(coins, cv2.COLOR_BGR2GRAY)
img = cv2.medianBlur(gray, 5)

# detect circles in the image
circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 20, 60,param1=50,param2=30,minRadius=0,maxRadius=0)
circles = np.uint16(np.around(circles))

# ensure at least some circles were found
if circles is not None:
	# convert the (x, y) coordinates and radius of the circles to integers
	circles = np.round(circles[0, :]).astype("int")
	# loop over the (x, y) coordinates and radius of the circles
	for (x, y, r) in circles:
		# draw the circle in the output image, then draw a rectangle
		# corresponding to the center of the circle
		cv2.circle(output, (x, y), r, (0, 255, 0), 4)
		cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
	# show the output image
	cv2.imshow("output", np.hstack([coins, output]))
	cv2.waitKey(0)