import cv2
import numpy as np
from skimage.util import random_noise

def detect_coins():
    # defining minimal and maximal radius, specified to the coins.jpg
    min_r = 150
    max_r = 300

    # preprocessing the input image
    coins = cv2.imread('input_image/4.jpg',0)
    orig = coins.copy()
    # noise_img = random_noise(coins, mode="s&p",amount=0.3)
    # noise_img = np.array(255*noise_img, dtype = 'uint8')
    img = cv2.medianBlur(coins,5)
    cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

    # circles = cv2.HoughCircles(
    #     img,                    # source image
    #     cv2.HOUGH_GRADIENT,     # type of detection
    #     1,                      # always 1
    #     300,                    # min distance between centers
    #     param1=30,              # adjust 1
    #     param2=100,             # adjust 2
    #     minRadius=min_r,        # minimal radius
    #     maxRadius=max_r,        # max radius
    # )
    circles = cv2.HoughCircles(
        img,                    # source image
        cv2.HOUGH_GRADIENT,     # type of detection
        1,                      # always 1
        300,                    # min distance between centers
        param1=35,              # adjust 1
        param2=80,             # adjust 2
        minRadius=min_r,        # minimal radius
        maxRadius=max_r,        # max radius
    )
    circles = np.uint16(np.around(circles))

    coins_copy = coins.copy()


    for detected_circle in circles[0]:
        x_coor, y_coor, detected_radius = detected_circle
        coins_detected = cv2.circle(
            coins_copy,
            (int(x_coor), int(y_coor)),
            int(detected_radius),
            (0, 255, 0),
            4,
        )
        cv2.putText(coins_detected,'radio: {}'.format(detected_radius),(x_coor -120,y_coor),cv2.FONT_HERSHEY_SIMPLEX,2,(0, 0, 0), 4)

    cv2.imwrite("output_image/coin_amount/euro_radio.jpg", coins_detected)

    return circles

def calculate_amount():
    monedas = {
        "1 C": {
            "value": 1,
            "radius": 16.26,
            "ratio": 1,
            "count": 0,
        },
        "2 C": {
            "value": 2,
            "radius": 18.75,
            "ratio": 1.153,
            "count": 0,
        },
        "5 C": {
            "value": 5,
            "radius": 21.25,
            "ratio": 1.306,
            "count": 0,
        },
        "10 C": {
            "value": 10,
            "radius": 19.75,
            "ratio": 1.214,
            "count": 0,
        },
        "20 C": {
            "value": 20,
            "radius": 22.25,
            "ratio": 1.368,
            "count": 0,
        },
        "50 C": {
            "value": 50,
            "radius": 24.25,
            "ratio": 1.491,
            "count": 0,
        },
        "1 E": {
            "value": 100,
            "radius": 23.25,
            "ratio": 1.429,
            "count": 0,
        },
        "2 E": {
            "value": 200,
            "radius": 25.75,
            "ratio": 1.583,
            "count": 0,
        },
    }

    circles = detect_coins()
    radius = []
    coordinates = []

    for detected_circle in circles[0]:
        x_coor, y_coor, detected_radius = detected_circle
        radius.append(detected_radius)
        coordinates.append([x_coor, y_coor])

    smallest = min(radius)
    tolerance = 0.032
    total_amount = 0

    coins_circled = cv2.imread('output_image/coin_amount/euro_radio.jpg', 1)
    font = cv2.FONT_HERSHEY_SIMPLEX

    for coin in circles[0]:
        ratio_to_check = coin[2] / smallest
        coor_x = coin[0]
        coor_y = coin[1]
        for euro in monedas:
            value = monedas[euro]['value']
            if abs(ratio_to_check - monedas[euro]['ratio']) <= tolerance:
                monedas[euro]['count'] += 1
                total_amount += monedas[euro]['value']
                cv2.putText(coins_circled, 'valor: {}'.format(value), (int(coor_x) -120 , int(coor_y)+ 100), font, 2,
                            (0, 0, 255), 4)

    print(f"El valor total es: {total_amount} Centimos")
    for euro in monedas:
        pieces = monedas[euro]['count']
        print(f"{euro} = {pieces}x")
    
    cv2.imwrite("output_image/coin_amount/euro_valor.jpg", coins_circled)

