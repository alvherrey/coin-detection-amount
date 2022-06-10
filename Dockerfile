FROM python:3.9
WORKDIR /app
RUN apt-get update && apt-get install --no-install-recommends -q -y ffmpeg libsm6 libxext6 software-properties-common
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY app .
CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8002"]