from board import process_chessboard_image
from model_tflite import get_positions
from fen import fen


models = {
    'Modelo A': 'weights//yolov8s_150ep_miDataset_float32.tflite',
    'Modelo B': 'weights//modelo_b_dataset_float32.tflite',
}


def main(image_path,punto_vista,model_name):

    warped_image = process_chessboard_image(image_path)
    detected_positions = get_positions(models[model_name],warped_image)
    generated_fen = fen(detected_positions,punto_vista)

    return generated_fen

