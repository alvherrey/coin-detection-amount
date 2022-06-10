import cv2
import numpy as np
from resize_image import image_resize

def detect_coins():
    coins = cv2.imread('input_image/6.jpg', 1)

    gray = cv2.cvtColor(coins, cv2.COLOR_BGR2GRAY)
    img = cv2.medianBlur(gray, 7)
    circles = cv2.HoughCircles(
        img,  # source image
        cv2.HOUGH_GRADIENT,  # type of detection
        1,
        40,
        param1=1,
        param2=30,
        minRadius=10,  # minimal radius
        maxRadius=200,  # max radius
    )

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
    tolerance = 0.03
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
                cv2.putText(coins_circled, str(value), (int(coor_x), int(coor_y)), font, 1,
                            (0, 0, 0), 4)

    print(f"El valor total es: {total_amount} Centimos")
    for euro in monedas:
        pieces = monedas[euro]['count']
        print(f"{euro} = {pieces}x")
    
    cv2.imwrite("output_image/coin_amount/euro_valor.jpg", coins_circled)

