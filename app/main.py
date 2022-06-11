from fastapi import FastAPI, UploadFile
from io import BytesIO
from PIL import Image
import numpy as np

from predict_coins import calculate_amount

app = FastAPI()

def load_image_into_numpy_array(data):
    return np.array(Image.open(BytesIO(data)))

@app.post("/coins/predict")
async def identify(file: UploadFile):
    img = load_image_into_numpy_array(await file.read())
    return calculate_amount(img)