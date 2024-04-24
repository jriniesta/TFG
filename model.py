from board import detect_chessboard_contour, four_point_transform
from ultralytics import YOLO
import cv2
import os
import glob

def find_latest_predict_directory(base_path):
    directories = [os.path.join(base_path, d) for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    latest_dir = max(directories, key=os.path.getmtime, default=None)
    return latest_dir

def get_positions(transformed_image_path):
    model = YOLO('best.pt')

    # Procesa la imagen transformada con el modelo YOLO
    results = model(transformed_image_path, save=True, save_txt=True, save_conf=True, conf=0.1)

    # Encuentra el directorio predict más reciente que contiene los resultados de la detección
    latest_dir = find_latest_predict_directory('runs/detect')
    if latest_dir is None:
        print("No se encontraron directorios de detección.")
        return None

    # Encuentra el archivo .txt dentro del último directorio
    label_path = os.path.join(latest_dir, 'labels', 'warped_chessboard.txt')
    if os.path.exists(label_path):
        print("Archivo de etiquetas encontrado:", label_path)
        return label_path
    else:
        print("No se encontró el archivo de etiquetas esperado.")
        return None
