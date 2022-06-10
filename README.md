# coin-detection-amount
Detecta las monedas y calcula el valor total en base a su radio.

## Referencias
### Paginas web
https://dev.to/tinazhouhui/discovering-open-cv-using-python-2iak
https://pyimagesearch.com/2014/07/21/detecting-circles-images-using-opencv-hough-circles/
https://dev.to/tinazhouhui/coin-detection-discovering-opencv-with-python-1ka1
https://dev.to/tinazhouhui/coin-amount-calculation-discovering-opencv-with-python-52gn
https://docs.opencv.org/4.x/d3/de5/tutorial_js_houghcircles.html

## Requerimientos
### Crear un entorno virtual con Miniconda
Creamos un entorno nuevo con python 3.8
```bash
conda create --name coin-detecion-amount python=3.8
```
Activamos el entorno
```bash
conda activate coin-detecion-amount
```
Instalar requiremets
```bash
pip install -r requirements.txt
```
## Ejecucion
### Uvicorn
Levantar el api con uvicorn
```bash
uvicorn app.main:app --reload
```
Acceder al swagger para probar
```bash
http://127.0.0.1:8000/docs#/
```
### Docker
```bash
sudo docker-compose build
sudo docker-compose up -d
```
