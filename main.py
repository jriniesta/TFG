from board import process_chessboard_image
from model import get_positions
from fen import fen






def main(image_path,punto_vista):
    warped_image = process_chessboard_image(image_path)
    detected_positions = get_positions(warped_image)
    generated_fen = fen(detected_positions,punto_vista)

    return generated_fen


if __name__ == '__main__':

    image_path = 'test_images/4.jpg'  # Ruta a la imagen de entrada
    punto_vista = 'lateral2'  # Perspectiva desde la que se ve el tablero
    print(main(image_path, punto_vista))