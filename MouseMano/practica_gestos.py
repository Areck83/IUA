#Issac Glez

#Importacion de librerias
#OpenCV: Libreria de visión por computadora libre
#Ayuda al reconocimiento de imágenes y la detección de rostros
import cv2

#Mediapipe
#Solución de manos de 21 puntos de referencia, detecta las manos y dedos
import mediapipe as mp

#numpy
#Biblioteca para crear vectores y matrices
import numpy as np

#Pyautogui
#Biblioteca para administrar o utilizar operaciones del mouse y del teclado
import pyautogui

#____________________________________________________________________________
#instanciamos la solución de mediapipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils #Para dibujar puntos en las manos

#Configurar la captura de video con OpenCV
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

#Definir los puntos de la pantalla
PANTALLA_X_INI = 0
PANTALLA_Y_INI = 0
PANTALLA_X_FIN = 1800
PANTALLA_Y_FIN = 900

#Definir el color del puntero
color_mouse = (255,0,255)

relacion_aspecto = (PANTALLA_X_FIN - PANTALLA_X_INI) / (PANTALLA_Y_FIN - PANTALLA_Y_INI)

#Margen del área azul
X_Y_INI = 100

#Gracias a omes
def calculate_distance(x1, y1, x2, y2):
    p1 = np.array([x1,y1])
    p2 = np.array ([x2,y2])
    return np.linalg.norm(p1-p2)


def detect_finger_down(hand_landmarks):
    finger_down = False
    color_base = (255,0,112)
    color_index = (255,198,82)

    x_base1 = int(hand_landmarks.landmark[0].x * width)
    y_base1 = int(hand_landmarks.landmark[0].y + height)

    x_base2 = int(hand_landmarks.landmark[9].x * width)
    y_base2 = int(hand_landmarks.landmark[9].y * height)

    x_index = int(hand_landmarks.landmark[8].x * width)
    y_index = int(hand_landmarks.landmark[8].y * height)

    d_base = calculate_distance(x_base1, y_base1, x_base2, y_base2)
    d_base_index = calculate_distance(x_base1, y_base1, x_index, y_index)

    if d_base_index < d_base:
        finger_down = True
        color_base = (255,0,255)
        color_index = (255,0,255)

    cv2.circle(output, (x_base1, y_base1), 5, color_base, 2)
    cv2.circle(output, (x_index, y_index), 5, color_index, 2)
    cv2.line(output, (x_base1, y_base1), (x_base2, y_base2), color_base, 3)
    cv2.line(output, (x_base1, y_base1), (x_index, y_index), color_index, 3)

    return finger_down

with mp_hands.Hands(
    static_image_mode = False,
    max_num_hands = 1, 
    min_detection_confidence = 0.5) as hands:

    while True:
        #Crear la ventana
        ret, frame = cap.read()
        if ret == False:
            break
        height, width, _ = frame.shape
        frame = cv2.flip(frame, 1)

        #Dibujamos el area proporcional
        area_width = width - X_Y_INI * 2
        area_height = int(area_width / relacion_aspecto)
        aux_image = np.zeros(frame.shape, np.uint8)

        #Crear el recuadro con los puntos encontrados
        aux_image = cv2.rectangle(aux_image, (X_Y_INI, X_Y_INI), (X_Y_INI + area_width, X_Y_INI + area_height), (255,0,0,0), -1)
        output = cv2.addWeighted(frame, 1, aux_image, 0.7, 0)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resultado = hands.process(frame_rgb)

        #Si detecta una mano
        if resultado.multi_hand_landmarks is not None:
            for hand_landmarks in resultado.multi_hand_landmarks:
                #Obtener las coordenadas de la mano
                x = int(hand_landmarks.landmark[9].x * width)
                y = int(hand_landmarks.landmark[9].y * height)
                xm = np.interp(x, (X_Y_INI, X_Y_INI + area_width), (PANTALLA_X_INI, PANTALLA_X_FIN))
                ym = np.interp(y, (X_Y_INI, X_Y_INI + area_height), (PANTALLA_Y_INI, PANTALLA_Y_FIN)) 

                #Mover el mouse
                pyautogui.moveTo(int(xm), int(ym))
                if detect_finger_down(hand_landmarks):
                    pyautogui.click()
                #Poner el circulo a donde movimos la mano
                cv2.circle(output, (x,y), 10, color_mouse, 3)
                cv2.circle(output, (x,y), 5, color_mouse, -1)

        #Mostrar pantalla
        cv2.imshow('output', output)

        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release
cv2.destroyAllWindows()