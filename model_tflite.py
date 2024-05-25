import tensorflow as tf
import numpy as np
import cv2
import os

confidence_threshold = 0.5
iou_threshold = 0.5

CLASSES = {
    0: 'bishop',
    1: 'black bishop',
    2: 'black king',
    3: 'black knight',
    4: 'black pawn',
    5: 'black queen',
    6: 'black rook',
    7: 'white bishop',
    8: 'white king',
    9: 'white knight',
    10: 'white pawn',
    11: 'white queen',
    12: 'white rook'
}

def get_positions(model_path, img_name):
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    image = cv2.imread(img_name)
    if image is None:
        raise ValueError(f"Could not load the image from {img_name}")

    image_height = input_details[0]['shape'][1]
    image_width = input_details[0]['shape'][2]
    resized_image = cv2.resize(image, (image_width, image_height))

    input_image = np.array(resized_image, dtype=np.float32) / 255.0
    input_image = input_image[np.newaxis, :]

    interpreter.set_tensor(input_details[0]['index'], input_image)
    interpreter.invoke()

    output = interpreter.get_tensor(output_details[0]['index'])
    output = output[0]
    output = output.T

    boxes_xywh = output[..., :4]
    scores = np.max(output[..., 4:], axis=1)
    classes = np.argmax(output[..., 4:], axis=1)

    indices = cv2.dnn.NMSBoxes(boxes_xywh.tolist(), scores.tolist(), confidence_threshold, iou_threshold)

    if len(indices) == 0 or isinstance(indices, tuple):
        os.remove(img_name)
        return []

    indices = indices.flatten()

    results = []
    for i in indices:
        if scores[i] >= confidence_threshold:
            x_center, y_center, width, height = boxes_xywh[i]
            x_center *= (image_width / image_width)
            y_center *= (image_height / image_height)
            width *= (image_width / image_width)
            height *= (image_height / image_height)

            result = {
                'class_id': classes[i],
                'class_name': CLASSES[classes[i]],
                'x_center': x_center,
                'y_center': y_center,
                'width': width,
                'height': height,
                'confidence': scores[i]
            }
            results.append(result)

    os.remove(img_name)
    
    return results