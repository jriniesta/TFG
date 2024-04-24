class PiezasAjedrez:
    def __init__(self):
        self.nombres = [
            'bishop', 'black-bishop', 'black-king', 'black-knight', 'black-pawn',
            'black-queen', 'black-rook', 'white-bishop', 'white-king',
            'white-knight', 'white-pawn', 'white-queen', 'white-rook'
        ]

    def obtener_nombre_pieza(self, indice):
        return self.nombres[indice]

piezas_ajedrez = PiezasAjedrez()

def procesar_etiqueta_yolo(linea, tamano_tablero=640, num_casillas=8, mapeo_piezas=piezas_ajedrez, punto_vista='blanco'):
    partes = linea.strip().split()
    indice_clase = int(partes[0])
    nombre_clase = mapeo_piezas.obtener_nombre_pieza(indice_clase)

    x_center_norm = float(partes[1])
    y_center_norm = float(partes[2])
    width_norm = float(partes[3])
    height_norm = float(partes[4])
    confianza = float(partes[5])

    x_center_px = x_center_norm * tamano_tablero
    y_center_px = y_center_norm * tamano_tablero
    width_px = width_norm * tamano_tablero
    height_px = height_norm * tamano_tablero

    x1 = x_center_px - width_px / 2
    x2 = x_center_px + width_px / 2
    y1 = y_center_px - height_px / 2
    y2 = y_center_px + height_px / 2

    # Usar el punto medio entre el centro y el borde inferior
    y_mid_point = (y_center_px + y2) / 2

    casilla_tamano = tamano_tablero / num_casillas
    columna = int(x_center_px // casilla_tamano)
    fila_mid = num_casillas - int(y_mid_point // casilla_tamano) - 1

    if punto_vista == 'blanco':
        columna_letra = chr(columna + 97)
        fila_numero = fila_mid + 1
    elif punto_vista == 'negro':
        columna_letra = chr((7 - columna) + 97)
        fila_numero = num_casillas - fila_mid
    elif punto_vista == 'lateral1':
        columna_letra = chr(fila_mid + 97)
        fila_numero = num_casillas - columna
    elif punto_vista == 'lateral2':
        columna_letra = chr((7 - fila_mid) + 97)
        fila_numero = columna + 1

    return {
        'clase': nombre_clase,
        'x1': x1, 'x2': x2,
        'y1': y1, 'y2': y2,
        'confianza': confianza,
        'fila': fila_numero,
        'columna': columna_letra,
        'notacion_ajedrez': f"{columna_letra}{fila_numero}"
    }


def procesar_etiquetas_de_archivo(ruta_archivo, punto_vista):

    etiquetas_procesadas = []
    with open(ruta_archivo, 'r') as archivo:
        for linea in archivo:
            etiqueta_procesada = procesar_etiqueta_yolo(linea, punto_vista=punto_vista)
            etiquetas_procesadas.append(etiqueta_procesada)
    return etiquetas_procesadas




def seleccionar_mejor_deteccion_por_casilla(detecciones):
    detecciones_por_casilla = {}
    for deteccion in detecciones:
        casilla = deteccion['notacion_ajedrez']
        if casilla not in detecciones_por_casilla:
            detecciones_por_casilla[casilla] = deteccion
        else:
            if deteccion['confianza'] > detecciones_por_casilla[casilla]['confianza']:
                detecciones_por_casilla[casilla] = deteccion


    return list(detecciones_por_casilla.values())






def extraer_posiciones_piezas(detecciones):
    posiciones_piezas = []
    for det in detecciones:
        pieza = det['clase']
        posicion = det['notacion_ajedrez']
        posiciones_piezas.append((pieza, posicion))


    return posiciones_piezas





import chess

def crear_fen_con_chess(posiciones_piezas):
    board = chess.Board(None)
    piece_map = {
        'white-king': chess.KING, 'black-king': chess.KING,
        'white-queen': chess.QUEEN, 'black-queen': chess.QUEEN,
        'white-rook': chess.ROOK, 'black-rook': chess.ROOK,
        'white-bishop': chess.BISHOP, 'black-bishop': chess.BISHOP,
        'white-knight': chess.KNIGHT, 'black-knight': chess.KNIGHT,
        'white-pawn': chess.PAWN, 'black-pawn': chess.PAWN
    }
    color_map = {
        'white': chess.WHITE,
        'black': chess.BLACK
    }

    # Colocar las piezas en el tablero
    for pieza, posicion in posiciones_piezas:
        color = color_map[pieza.split('-')[0]]
        piece_type = piece_map[pieza]
        square = chess.parse_square(posicion.lower())
        board.set_piece_at(square, chess.Piece(piece_type, color))

    return board.fen()




def fen(ruta_archivo,punto_vista):

    etiquetas = procesar_etiquetas_de_archivo(ruta_archivo, punto_vista)
    mejores_detecciones = seleccionar_mejor_deteccion_por_casilla(etiquetas)
    posiciones = extraer_posiciones_piezas(mejores_detecciones)

    fen = crear_fen_con_chess(posiciones)

    return fen

