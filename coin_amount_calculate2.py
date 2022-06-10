import cv2
import numpy as np
from resize_image import image_resize

def detect_coins():
    # defining minimal and maximal radius, specified to the coins.jpg
    min_r = 10
    max_r = 50

    img = cv2.imread('input_image/6.jpg',0)
    img = image_resize(img, width =  250)
    orig = img.copy()
    img = cv2.medianBlur(img,5)
    # cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

    # extract the circles
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 40, param1=40, param2=30, minRadius=min_r, maxRadius=max_r)
    circles = np.uint16(np.around(circles))

    # ensure at least some circles were found
    if circles is not None:
        # loop over the (x, y) coordinates and radius of the circles
        for i in circles[0,:]:
            # draw the outer circle
            cv2.circle(orig,(i[0],i[1]),i[2],(0,255,0),1)
            # draw the center of the circle
            cv2.circle(orig,(i[0],i[1]),2,(0,0,255),3)
            cv2.putText(orig,'{}'.format(i[2]),(i[0],i[1]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0))
            print('radio:{}'.format(i[2]))

    
    cv2.imwrite("output_image/coin_amount/euro_radio.jpg", orig)
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
    # font = cv2.FONT_HERSHEY_SIMPLEX

    for coin in circles[0]:
        ratio_to_check = coin[2] / smallest
        # coor_x = coin[0]
        # coor_y = coin[1]
        for euro in monedas:
            # value = monedas[euro]['value']
            if abs(ratio_to_check - monedas[euro]['ratio']) <= tolerance:
                monedas[euro]['count'] += 1
                # total_amount += monedas[euro]['value']
                # cv2.putText(coins_circled, str(value), (int(coor_x), int(coor_y)), font, 1,
                #             (0, 0, 0), 4)

    # print(f"El valor total es: {total_amount} Centimos")
    # for euro in monedas:
    #     pieces = monedas[euro]['count']
    #     print(f"{euro} = {pieces}x")
    
    # cv2.imwrite("output_image/coin_amount/euro_valor.jpg", coins_circled)
    return monedas

