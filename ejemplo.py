import cv2
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from main_model import main

class CameraApp(App):
    def build(self):
        self.img = Image()
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.img)

        self.capture = cv2.VideoCapture(0)

        # Botón para salir de la aplicación
        self.button = Button(text="Salir", size_hint=(1, 0.1))
        self.button.bind(on_press=self.stop)
        layout.add_widget(self.button)

        Clock.schedule_interval(self.update, 1.0 / 30.0)
        return layout

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            # Procesar el frame con el método main
            processed_frame = main(frame,'Lateral 1')
            print(processed_frame)


    def main(self, frame):
        # Aquí puedes agregar tu lógica de procesamiento de imágenes
        # Por ejemplo, detección de bordes:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        return edges_colored

    def stop(self, *args):
        self.capture.release()
        super().stop(*args)


if __name__ == '__main__':
    CameraApp().run()