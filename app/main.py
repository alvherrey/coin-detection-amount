# from predict_coins import calculate_amount

# def main():
#     calculate_amount()

# if __name__ == "__main__":
#     main()



from fastapi import FastAPI, UploadFile
from io import BytesIO
from PIL import Image
import numpy as np
import cv2

from predict_coins import calculate_amount

app = FastAPI()

def load_image_into_numpy_array(data):
    return np.array(Image.open(BytesIO(data)))

# def load_image_into_numpy_array(data):
#     npimg=np.frombuffer(data,np.uint8)
#     frame=cv2.imdecode(npimg,cv2.IMREAD_COLOR)
#     return cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

@app.post("/coins/predict")
async def identify(file: UploadFile):
    img = load_image_into_numpy_array(await file.read())
    return calculate_amount(img)