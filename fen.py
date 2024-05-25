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

def procesar_etiqueta_yolo(etiqueta, tamano_tablero=640, num_casillas=8, mapeo_piezas=piezas_ajedrez, punto_vista='blanco'):
    nombre_clase = mapeo_piezas.obtener_nombre_pieza(etiqueta['class_id'])

    x_center_px = etiqueta['x_center'] * tamano_tablero
    y_center_px = etiqueta['y_center'] * tamano_tablero
    width_px = etiqueta['width'] * tamano_tablero
    height_px = etiqueta['height'] * tamano_tablero

    x1 = x_center_px - width_px / 2
    x2 = x_center_px + width_px / 2
    y1 = y_center_px - height_px / 2
    y2 = y_center_px + height_px / 2

    # Usar el punto medio entre el centro y el borde inferior
    y_mid_point = (y_center_px + y2) / 2
    casilla_tamano = tamano_tablero / num_casillas
    columna = int(x_center_px // casilla_tamano)
    fila_mid = num_casillas - int(y_mid_point // casilla_tamano) - 1

    if punto_vista == 'Blanco':
        columna_letra = chr(columna + 97)
        fila_numero = fila_mid + 1
    elif punto_vista == 'Negro':
        columna_letra = chr((7 - columna) + 97)
        fila_numero = num_casillas - fila_mid
    elif punto_vista == 'Lateral 1':
        columna_letra = chr((7 - fila_mid) + 97)
        fila_numero = columna + 1
    elif punto_vista == 'Lateral 2':
        columna_letra = chr(fila_mid + 97)
        fila_numero = num_casillas - columna


    return {
        'clase': nombre_clase,
        'x1': x1, 'x2': x2,
        'y1': y1, 'y2': y2,
        'confianza': etiqueta['confidence'],
        'fila': fila_numero,
        'columna': columna_letra,
        'notacion_ajedrez': f"{columna_letra}{fila_numero}"
    }

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

def crear_fen_con_chess(posiciones_piezas):
    tablero = [[" " for _ in range(8)] for _ in range(8)]
    fen_piezas = {
        'white-king': 'K', 'black-king': 'k',
        'white-queen': 'Q', 'black-queen': 'q',
        'white-rook': 'R', 'black-rook': 'r',
        'white-bishop': 'B', 'black-bishop': 'b',
        'white-knight': 'N', 'black-knight': 'n',
        'white-pawn': 'P', 'black-pawn': 'p'
    }
    
    for pieza, posicion in posiciones_piezas:
        columna = ord(posicion[0]) - ord('a')
        fila = 8 - int(posicion[1])
        tablero[fila][columna] = fen_piezas[pieza]
    
    fen = ""
    for fila in tablero:
        vacias = 0
        for celda in fila:
            if celda == " ":
                vacias += 1
            else:
                if vacias > 0:
                    fen += str(vacias)
                    vacias = 0
                fen += celda
        if vacias > 0:
            fen += str(vacias)
        fen += "/"
    
    fen = fen[:-1] + " w - - 0 1"
    
    return fen

def fen(detecciones, punto_vista):
    procesadas = [procesar_etiqueta_yolo(det, punto_vista=punto_vista) for det in detecciones]
    mejores_detecciones = seleccionar_mejor_deteccion_por_casilla(procesadas)
    posiciones = extraer_posiciones_piezas(mejores_detecciones)
    return crear_fen_con_chess(posiciones)

