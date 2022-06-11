from fastapi import FastAPI, UploadFile
from io import BytesIO
from PIL import Image
import numpy as np
import os

from predict_coins import calculate_amount

app = FastAPI()

def load_image_into_numpy_array(data):
    return np.array(Image.open(BytesIO(data)))

def print_env_variables():
    print('')
    print('MIN_COIN_RADIO: {}'.format(os.getenv('MIN_COIN_RADIO')))
    print('MAX_COIN_RADIO: {}'.format(os.getenv('MAX_COIN_RADIO')))
    print('MIN_COIN_DISTANCE: {}'.format(os.getenv('MIN_COIN_DISTANCE')))
    print('HOUGH_PARAM_1: {}'.format(os.getenv('HOUGH_PARAM_1')))
    print('HOUGH_PARAM_2: {}'.format(os.getenv('HOUGH_PARAM_2')))
    print('')

@app.post("/coins/predict")
async def identify(file: UploadFile):
    print_env_variables()
    img = load_image_into_numpy_array(await file.read())
    return calculate_amount(img)