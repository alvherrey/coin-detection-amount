import base64
import cv2
import numpy as np
import os

def detect_coins(input_img):

    # defining hough params from os env variable
    min_coin_radio = int(os.getenv('MIN_COIN_RADIO'))
    max_coin_radio = int(os.getenv('MAX_COIN_RADIO'))
    min_coin_distance = int(os.getenv('MIN_COIN_DISTANCE'))
    hough_param_1 = int(os.getenv('HOUGH_PARAM_1'))
    hough_param_2 = int(os.getenv('HOUGH_PARAM_2'))

    # preprocessing the input image
    cv2.imwrite("euro.jpg", input_img)
    coins = cv2.imread('euro.jpg',0)
    img = coins.copy()

    # get circles
    circles = cv2.HoughCircles(
        img,                                # source image
        cv2.HOUGH_GRADIENT,                 # type of detection
        1,                                  # always 1
        min_coin_distance,                  # min distance between centers
        param1=hough_param_1,               # adjust param 1
        param2=hough_param_2,               # adjust param 2
        minRadius=min_coin_radio,           # minimal radius
        maxRadius=max_coin_radio,           # max radius
    )
    if circles is None:
        print('es nulo')
        return
    circles = np.uint16(np.round(circles))

    # write radios to image
    coins_copy = coins.copy()
    for detected_circle in circles[0]:
        x_coor, y_coor, detected_radius = detected_circle
        coins_detected = cv2.circle(
            coins_copy,
            (int(x_coor), int(y_coor)),
            int(detected_radius),
            (255, 0, 0),
            2,
        )
        cv2.putText(coins_detected,'radio: {}'.format(detected_radius),(x_coor -60,y_coor),cv2.FONT_HERSHEY_SIMPLEX,1,(255, 0, 0), 2)
    cv2.imwrite("euro_radio.jpg", coins_detected)

    # return circles
    return circles

def calculate_amount(input_img):

    # monedas initial map
    monedas = {
        "coins" : 
            {
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
        },
    }

    circles = detect_coins(input_img)
    radius = []
    coordinates = []

    for detected_circle in circles[0]:
        x_coor, y_coor, detected_radius = detected_circle
        radius.append(detected_radius)
        coordinates.append([x_coor, y_coor])

    smallest = min(radius)
    tolerance = 0.032
    total_amount = 0

    coins_circled = cv2.imread('euro_radio.jpg', 1)
    font = cv2.FONT_HERSHEY_SIMPLEX

    # comprobacion de los ratios
    for coin in circles[0]:
        ratio_to_check = coin[2] / smallest
        coor_x = coin[0]
        coor_y = coin[1]
        for moneda in monedas['coins']:
            value = monedas['coins'][moneda]['value']
            if abs(ratio_to_check - monedas['coins'][moneda]['ratio']) <= tolerance:
                monedas['coins'][moneda]['count'] += 1
                total_amount += monedas['coins'][moneda]['value']
                cv2.putText(coins_circled, 'valor: {}'.format(value), (int(coor_x) -60 , int(coor_y)+ 30), font, 1,
                            (0, 0, 255), 2)

    # Guardar imagen del resultado
    cv2.imwrite("euro_valor.jpg", coins_circled)

    # encode a b64 de la imagen resultado
    with open("euro_valor.jpg", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

    # Añadir total amount y imagen al diccionario monedas
    monedas['total_amount'] = total_amount
    monedas['encoded_image'] = encoded_string

    # return monedas result map
    return monedas

