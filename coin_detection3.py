import cv2
import numpy as np

coins = cv2.imread('input_image/coins.jpg', 1)

# defining minimal and maximal radius, specified to the coins.jpg
min_r = 1
max_r = 100

def hough_circle_detection():
    gray = cv2.cvtColor(coins, cv2.COLOR_BGR2GRAY)
    img = cv2.medianBlur(gray, 5)
    circles = cv2.HoughCircles(
        img,  # source image
        cv2.HOUGH_GRADIENT,  # type of detection
        1,
        40,
        param1=50,
        param2=30,
        minRadius=min_r*2,  # minimal radius
        maxRadius=max_r*2,  # max radius
    )

    coins_copy = coins.copy()

    for detected_circle in circles[0]:
        x_coor, y_coor, detected_radius = detected_circle
        coins_detected = cv2.circle(coins_copy, (x_coor, y_coor), detected_radius, (0, 0, 255), 1)

    cv2.imwrite("output_image/coin_detection/coins_detected_Hough.jpg", coins_detected)

