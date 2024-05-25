import cv2
import numpy as np
from datetime import datetime

def detect_chessboard_contour(input_data):
    # Comprueba si el input es un path de imagen o un frame directamente
    if isinstance(input_data, str):
        # Asume que es una ruta de imagen y trata de cargarla
        original_img = cv2.imread(input_data)
        if original_img is None:
            print("Error: No se pudo cargar la imagen desde la ruta proporcionada.")
            return None, None
    elif isinstance(input_data, np.ndarray):
        # Asume que es un frame directo y lo utiliza tal cual
        original_img = input_data
    else:
        print("Tipo de entrada no reconocido.")
        return None, None

    img = original_img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    edges = cv2.Canny(thresh, 50, 150, apertureSize=3)
    dilated = cv2.dilate(edges, np.ones((3, 3), np.uint8), iterations=1)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        return largest_contour, original_img  # Devuelve el contorno más grande y la imagen original
    else:
        print("No se encontraron contornos.")
        return None, original_img


def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect

def four_point_transform(image, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    # Ajusta el destino para la transformación de perspectiva
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    # Realiza la transformación de perspectiva
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    
    return warped


def process_chessboard_image(image_path):
    largest_contour, original_img = detect_chessboard_contour(image_path)
    if largest_contour is not None:
        pts = largest_contour.reshape(-1, 2)
        warped_image = four_point_transform(original_img, pts)

        # Crea un nombre de archivo único basado en la fecha y hora actuales
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = f'test_images//warped_chessboard_{timestamp}.jpg'

        cv2.imwrite(save_path, warped_image)  # Guarda la imagen en el sistema de archivos
        return save_path
    else:
        print("El contorno del tablero de ajedrez no está definido.")
        return None
