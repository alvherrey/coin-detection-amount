import cv2
import numpy as np
import base64

def detect_coins(input_img):

    # defining minimal and maximal radius, specified to the coins.jpg
    min_r = 100
    max_r = 300

    # preprocessing the input image
    cv2.imwrite("euro.jpg", input_img)

    coins = cv2.imread('euro.jpg',0)

    img = cv2.medianBlur(coins,5)

    # get hough circles
    # circles = cv2.HoughCircles(
    #     img,                    # source image
    #     cv2.HOUGH_GRADIENT,     # type of detection
    #     1,                      # always 1
    #     300,                    # min distance between centers
    #     param1=35,              # adjust 1
    #     param2=80,             # adjust 2
    #     minRadius=min_r,        # minimal radius
    #     maxRadius=max_r,        # max radius
    # )
    # circles = cv2.HoughCircles(
    #     img,                    # source image
    #     cv2.HOUGH_GRADIENT,     # type of detection
    #     1,                      # always 1
    #     300,                    # min distance between centers
    #     param1=100,              # adjust 1
    #     param2=50,             # adjust 2
    #     minRadius=min_r,        # minimal radius
    #     maxRadius=max_r,        # max radius
    # )
    circles = cv2.HoughCircles(
        img,                    # source image
        cv2.HOUGH_GRADIENT,     # type of detection
        1,                      # always 1
        250,                    # min distance between centers
        param1=130,              # adjust 1
        param2=60,             # adjust 2
        minRadius=min_r,        # minimal radius
        maxRadius=max_r,        # max radius
    )
    circles = np.uint16(np.around(circles))

    # write radios to image
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
    cv2.imwrite("euro_radio.jpg", coins_detected)

    # return circles
    return circles

def calculate_amount(input_img):

    # monedas initial map
    # monedas = {
    #     "1 C": {
    #         "value": 1,
    #         "radius": 16.26,
    #         "ratio": 1,
    #         "count": 0,
    #     },
    #     "2 C": {
    #         "value": 2,
    #         "radius": 18.75,
    #         "ratio": 1.153,
    #         "count": 0,
    #     },
    #     "5 C": {
    #         "value": 5,
    #         "radius": 21.25,
    #         "ratio": 1.306,
    #         "count": 0,
    #     },
    #     "10 C": {
    #         "value": 10,
    #         "radius": 19.75,
    #         "ratio": 1.214,
    #         "count": 0,
    #     },
    #     "20 C": {
    #         "value": 20,
    #         "radius": 22.25,
    #         "ratio": 1.368,
    #         "count": 0,
    #     },
    #     "50 C": {
    #         "value": 50,
    #         "radius": 24.25,
    #         "ratio": 1.491,
    #         "count": 0,
    #     },
    #     "1 E": {
    #         "value": 100,
    #         "radius": 23.25,
    #         "ratio": 1.429,
    #         "count": 0,
    #     },
    #     "2 E": {
    #         "value": 200,
    #         "radius": 25.75,
    #         "ratio": 1.583,
    #         "count": 0,
    #     },
    # }
    monedas = {
        "1 C": {
            "value": 1,
            "radius": 16.3,
            "ratio": 1,
            "count": 0,
        },
        "2 C": {
            "value": 2,
            "radius": 18.8,
            "ratio": 1.153,
            "count": 0,
        },
        "5 C": {
            "value": 5,
            "radius": 21.35,
            "ratio": 1.309,
            "count": 0,
        },
        "10 C": {
            "value": 10,
            "radius": 19.8,
            "ratio": 1.214,
            "count": 0,
        },
        "20 C": {
            "value": 20,
            "radius": 22.3,
            "ratio": 1.368,
            "count": 0,
        },
        "50 C": {
            "value": 50,
            "radius": 24.3,
            "ratio": 1.490,
            "count": 0,
        },
        "1 E": {
            "value": 100,
            "radius": 23.3,
            "ratio": 1.429,
            "count": 0,
        },
        "2 E": {
            "value": 200,
            "radius": 25.8,
            "ratio": 1.583,
            "count": 0,
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
    tolerance = 0.035
    total_amount = 0

    coins_circled = cv2.imread('euro_radio.jpg', 1)
    font = cv2.FONT_HERSHEY_SIMPLEX

    # comprobacion de los ratios
    for coin in circles[0]:
        ratio_to_check = coin[2] / smallest
        coor_x = coin[0]
        coor_y = coin[1]
        for moneda in monedas:
            value = monedas[moneda]['value']
            if abs(ratio_to_check - monedas[moneda]['ratio']) <= tolerance:
                monedas[moneda]['count'] += 1
                total_amount += monedas[moneda]['value']
                cv2.putText(coins_circled, 'valor: {}'.format(value), (int(coor_x) -120 , int(coor_y)+ 100), font, 2,
                            (0, 0, 255), 4)

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

