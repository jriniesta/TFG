class Posicion:

    def __init__(self, imagen, descripcion, fen, punto_vista):
        self.imagen = imagen
        self.descripcion = descripcion
        self.fen = fen
        self.punto_vista = punto_vista

    def actualizar_fen(self, nuevo_fen):
        self.fen = nuevo_fen



def crear_posiciones():
    image_path_template = 'test_images//{}.jpg'
    # Ahora cada posición se inicializa con 'Lateral 2' como punto de vista
    posiciones = [Posicion(image_path_template.format(i), f'Descripción {i}', '', 'Lateral 2') for i in range(1, 25)]
    
    return posiciones

