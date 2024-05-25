import os
import threading
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp, sp
from kivy.uix.image import Image
from kivy.clock import mainthread
from kivy.uix.gridlayout import GridLayout
from kivy.core.text import LabelBase
from kivy.uix.camera import Camera
from fen_manager import FenManager
from main_model import main
from posiciones import crear_posiciones
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.clock import Clock
from kivy.uix.popup import Popup
import webbrowser
import cv2
from kivy.graphics.texture import Texture
import time
import cv2
from kivy.graphics.texture import Texture
import time
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.config import Config
from kivy.uix.spinner import Spinner
from kivy.graphics import Rectangle, Color
from plyer import filechooser, storagepath, camera
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image
from kivy.base import EventLoop
import numpy as np
from datetime import datetime
from kivymd.uix.button import MDFloatingActionButton
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.widget import Widget
# Request necessary permissions on Android

Window.size = (360, 640)  # Por ejemplo, una proporción de móvil común

try:
    from android.permissions import request_permissions, Permission
    request_permissions([
        Permission.CAMERA,
        Permission.WRITE_EXTERNAL_STORAGE,
        Permission.READ_EXTERNAL_STORAGE,
        Permission.INTERNET,
        Permission.BODY_SENSORS,
        Permission.BLUETOOTH
    ])
except Exception as e:
    print("No esta en Android")


LabelBase.register(name='roboto_normal', fn_regular='assets//fonts//RobotoCondensed-Bold.ttf')
LabelBase.register(name='roboto_titulo', fn_regular='assets//fonts//RobotoCondensed-Regular.ttf')




Builder.load_file('assets//kv//boton.kv')
Builder.load_file('assets//kv//boton_img.kv')
Builder.load_file('assets//kv//botongray.kv')



class HomeScreen(Screen):

    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))

        title_label = Label(
            text='Detector de Posiciones',
            font_size=sp(30),
            font_name="roboto_titulo",
            size_hint_y=0.1,
            color=(1, 1, 1, 1)
        )
        layout.add_widget(title_label)

        img = Image(source='assets/img/chessboard_home.png', keep_ratio=True, allow_stretch=True, size_hint=(1, 0.6))
        layout.add_widget(img)

        btn_scan = Factory.RoundedButton(text="Registro de posiciones")
        btn_scan.bind(on_press=self.go_to_position_choice)
        layout.add_widget(btn_scan)

        btn_live_analysis = Factory.RoundedButton(text="Análisis en Vivo")
        btn_live_analysis.bind(on_press=self.go_to_live_analysis)
        layout.add_widget(btn_live_analysis)

        btn_help = Factory.RoundedButton(text="Ayuda")
        btn_help.bind(on_press=self.go_to_help)
        layout.add_widget(btn_help)

        self.add_widget(layout)

    def go_to_help(self, instance):
        self.manager.transition.direction = 'left'
        self.manager.current = 'help_screen'

    def go_to_live_analysis(self, instance):
        self.loading_popup = LoadingPopup()
        self.loading_popup.open()
        Clock.schedule_once(self.start_live_analysis)

    def start_live_analysis(self, dt):
        self.manager.transition.direction = 'left'
        self.manager.current = 'live_analysis_screen'
        self.loading_popup.dismiss()

    def go_to_scan(self, instance):
        self.loading_popup = CustomPopup()
        self.loading_popup.open()
        Clock.schedule_once(self.start_position_scan)

    def start_position_scan(self, dt):
        self.manager.transition.direction = 'left'
        self.manager.current = 'positions_screen'
        self.loading_popup.dismiss()

    def go_to_position_choice(self, instance):
        self.manager.transition.direction = 'left'
        self.manager.current = 'position_choice'

class HelpScreen(Screen):
    def __init__(self, **kwargs):
        super(HelpScreen, self).__init__(**kwargs)
        layout = FloatLayout()

        padding_y = dp(10)
        
        title_label = Label(
            text='Ayuda',
            font_size=sp(30),
            font_name="roboto_titulo",
            size_hint=(0.8, None),
            height=dp(50),
            pos_hint={"center_x": 0.5, "top": 0.95}
        )
        layout.add_widget(title_label)

        btn_how_to_use = Factory.GrayRoundedButton(
            text="¿Cómo usar el detector de posiciones?",
            size_hint=(0.8, None),
            height=dp(50),
            pos_hint={"center_x": 0.5, "top": 0.75}
        )
        btn_how_to_use.bind(on_press=self.go_to_how_to_use)
        layout.add_widget(btn_how_to_use)

        btn_live_analysis_help = Factory.GrayRoundedButton(
            text="Modelos disponibles",
            size_hint=(0.8, None),
            height=dp(50),
            pos_hint={"center_x": 0.5, "top": 0.60}
        )
        btn_live_analysis_help.bind(on_press=self.go_to_live_analysis_help)
        layout.add_widget(btn_live_analysis_help)

        btn_contact_support = Factory.GrayRoundedButton(
            text="Resultados incorrectos",
            size_hint=(0.8, None),
            height=dp(50),
            pos_hint={"center_x": 0.5, "top": 0.45}
        )
        btn_contact_support.bind(on_press=self.go_to_contact_support)
        layout.add_widget(btn_contact_support)

        self.add_widget(layout)

    def go_to_how_to_use(self, instance):
        self.manager.transition.direction = 'left'
        self.manager.current = 'how_to_use_screen'

    def go_to_live_analysis_help(self, instance):
        self.manager.transition.direction = 'left'
        self.manager.current = 'modelos_help_screen'

    def go_to_contact_support(self, instance):
        self.manager.transition.direction = 'left'
        self.manager.current = 'contact_support_screen'

class HowToUseScreen(Screen):
    def __init__(self, **kwargs):
        super(HowToUseScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))

        title_label = Label(
            text='Cómo usar la aplicación',
            font_size=sp(30),
            font_name="roboto_titulo",
            size_hint_y=None,
            height=dp(40),
            color=(1, 1, 1, 1)
        )
        layout.add_widget(title_label)

        scroll_view = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        content_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10), size_hint_y=None)
        content_layout.bind(minimum_height=content_layout.setter('height'))

        content_text_1 = '''
        Para obtener buenos resultados al usar la aplicación, ya sea mediante detecciones con foto o vídeo, es importante considerar ciertos aspectos. Hay tres configuraciones clave para asegurar una detección correcta: el ángulo del tablero, quién mueve en la posición y el modelo utilizado para la detección.

        En primer lugar, es crucial cuidar los ángulos y la iluminación, intentando que esta sea la más adecuada según el modelo con el que se entrenó. Es esencial marcar el tipo de ángulo que se está utilizando, teniendo disponibles cuatro opciones: blanco, negro, lateral 1 (negro-blanco) y lateral 2 (blanco-negro).
        '''
        content_label_1 = Label(
            text=content_text_1,
            font_name="roboto_titulo",
            font_size=sp(20),
            size_hint_y=None,
            markup=True,
            color=(1, 1, 1, 1),
            text_size=(dp(300), None),
            halign='justify',
            valign='top'
        )
        content_label_1.bind(texture_size=content_label_1.setter('size'))
        content_layout.add_widget(content_label_1)

        # Add images with captions
        image_1 = Image(
            source='assets/img/tablero1.JPG',  # Update with the correct path to your image
            size_hint=(1, None),
            height=dp(200)
        )
        content_layout.add_widget(image_1)

        caption_1 = Label(
            text='Vista desde el lado blanco',
            font_size=sp(16),
            size_hint_y=None,
            height=dp(30),
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle'
        )
        caption_1.bind(texture_size=caption_1.setter('size'))
        content_layout.add_widget(caption_1)

        image_2 = Image(
            source='assets/img/tablero2.JPG',  # Update with the correct path to your image
            size_hint=(1, None),
            height=dp(200)
        )
        content_layout.add_widget(image_2)

        caption_2 = Label(
            text='Vista desde el lado negro',
            font_size=sp(16),
            size_hint_y=None,
            height=dp(30),
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle'
        )
        caption_2.bind(texture_size=caption_2.setter('size'))
        content_layout.add_widget(caption_2)

        image_3 = Image(
            source='assets/img/tablero3.JPG',  # Update with the correct path to your image
            size_hint=(1, None),
            height=dp(200)
        )
        content_layout.add_widget(image_3)

        caption_3 = Label(
            text='Vista lateral 1 (negro-blanco)',
            font_size=sp(16),
            size_hint_y=None,
            height=dp(30),
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle'
        )
        caption_3.bind(texture_size=caption_3.setter('size'))
        content_layout.add_widget(caption_3)

        image_4 = Image(
            source='assets/img/tablero4.JPG',  # Update with the correct path to your image
            size_hint=(1, None),
            height=dp(200)
        )
        content_layout.add_widget(image_4)

        caption_4 = Label(
            text='Vista lateral 2 (blanco-negro)',
            font_size=sp(16),
            size_hint_y=None,
            height=dp(30),
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle'
        )
        caption_4.bind(texture_size=caption_4.setter('size'))
        content_layout.add_widget(caption_4)

        content_text_2 = '''
        También es importante indicar quién mueve en la posición a detectar para asegurar la precisión de los resultados.

        Además, se le da a elegir el modelo sobre el cual se van a detectar las posiciones. Cada modelo se entrenó y, por lo tanto, reconoce mejor un set específico de piezas. Cada tipo de modelo se entrenó sobre un conjunto de ángulos que le ayudan a detectar mejor las posiciones que otros.

        Para más información sobre los modelos, consulte la sección específica relacionada.
        '''
        content_label_2 = Label(
            text=content_text_2,
            font_name="roboto_titulo",
            font_size=sp(20),
            size_hint_y=None,
            markup=True,
            color=(1, 1, 1, 1),
            text_size=(dp(300), None),
            halign='justify',
            valign='top'
        )
        content_label_2.bind(texture_size=content_label_2.setter('size'))
        content_layout.add_widget(content_label_2)

        scroll_view.add_widget(content_layout)
        layout.add_widget(scroll_view)

        self.add_widget(layout)

class ModelosHelpScreen(Screen):
    def __init__(self, **kwargs):
        super(ModelosHelpScreen, self).__init__(**kwargs)

        layout = FloatLayout()

        title_label = Label(
            text='Modelos Disponibles',
            font_size=sp(30),
            font_name="roboto_titulo",
            size_hint=(None, None),
            height=dp(40),
            color=(1, 1, 1, 1),
            pos_hint={'center_x': 0.5, 'top': 0.93}
        )
        layout.add_widget(title_label)

        content_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10), size_hint=(0.9, None), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        content_layout.bind(minimum_height=content_layout.setter('height'))

        content_text = '''
        La aplicación permite seleccionar entre diferentes modelos para la detección de posiciones. Cada modelo ha sido entrenado para reconocer un conjunto específico de piezas y ángulos, optimizando la precisión de las detecciones según el contexto de uso. A continuación, se presentan los modelos disponibles:
        '''
        content_label = Label(
            text=content_text,
            font_size=sp(20),
            size_hint_y=None,
            markup=True,
            color=(1, 1, 1, 1),
            text_size=(dp(300), None),
            halign='justify',
            valign='top'
        )
        content_label.bind(texture_size=content_label.setter('size'))
        content_layout.add_widget(content_label)

        spacer = Widget(size_hint_y=None, height=dp(10))
        content_layout.add_widget(spacer)

        # Add models buttons
        btn_model_a = Factory.GrayRoundedButton(
            text="Modelo A",
            size_hint=(1, None),
            height=dp(50)
        )
        btn_model_a.bind(on_press=self.go_to_model_a)
        content_layout.add_widget(btn_model_a)

        spacer = Widget(size_hint_y=None, height=dp(5))
        content_layout.add_widget(spacer)

        btn_model_b = Factory.GrayRoundedButton(
            text="Modelo B",
            size_hint=(1, None),
            height=dp(50)
        )
        btn_model_b.bind(on_press=self.go_to_model_b)
        content_layout.add_widget(btn_model_b)

        layout.add_widget(content_layout)


        self.add_widget(layout)

    def update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def go_to_model_a(self, instance):
        self.manager.transition.direction = 'left'
        self.manager.current = 'model_a_screen'

    def go_to_model_b(self, instance):
        self.manager.transition.direction = 'left'
        self.manager.current = 'model_b_screen'

class ModelAScreen(Screen):
    def __init__(self, **kwargs):
        super(ModelAScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))

        title_label = Label(
            text='Modelo A',
            font_size=sp(30),
            font_name="roboto_titulo",
            size_hint_y=None,
            height=dp(40),
            color=(1, 1, 1, 1)
        )
        layout.add_widget(title_label)

        scroll_view = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        content_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10), size_hint_y=None)
        content_layout.bind(minimum_height=content_layout.setter('height'))

        content_text_1 = '''
        A continuación, se muestran imágenes del Modelo A. Si tu set de piezas se parece a las usadas en este modelo, selecciónalo para tus detecciones.
        '''
        content_label_1 = Label(
            text=content_text_1,
            font_name="roboto_titulo",
            font_size=sp(20),
            size_hint_y=None,
            markup=True,
            color=(1, 1, 1, 1),
            text_size=(dp(300), None),
            halign='justify',
            valign='top'
        )
        content_label_1.bind(texture_size=content_label_1.setter('size'))
        content_layout.add_widget(content_label_1)

        # Add images with captions
        image_1 = Image(
            source='test_images/13.jpg',  # Update with the correct path to your image
            size_hint=(1, None),
            height=dp(200)
        )
        content_layout.add_widget(image_1)

        caption_1 = Label(
            text='Modelo A - Ejemplo 1',
            font_size=sp(16),
            size_hint_y=None,
            height=dp(30),
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle'
        )
        caption_1.bind(texture_size=caption_1.setter('size'))
        content_layout.add_widget(caption_1)

        image_2 = Image(
            source='test_images/8.jpg',  # Update with the correct path to your image
            size_hint=(1, None),
            height=dp(200)
        )
        content_layout.add_widget(image_2)

        caption_2 = Label(
            text='Modelo A - Ejemplo 2',
            font_size=sp(16),
            size_hint_y=None,
            height=dp(30),
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle'
        )
        caption_2.bind(texture_size=caption_2.setter('size'))
        content_layout.add_widget(caption_2)

        image_3 = Image(
            source='test_images/12.jpg',  # Update with the correct path to your image
            size_hint=(1, None),
            height=dp(200)
        )
        content_layout.add_widget(image_3)

        caption_3 = Label(
            text='Modelo A - Ejemplo 3',
            font_size=sp(16),
            size_hint_y=None,
            height=dp(30),
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle'
        )
        caption_3.bind(texture_size=caption_3.setter('size'))
        content_layout.add_widget(caption_3)



        content_text_2 = '''
        Como puedes observar, el ángulo usado es 'Lateral 1' (blanco-negro). Por lo tanto, si utilizas este dataset, funcionará mejor desde un ángulo lateral, ya sea 'Lateral 1' o 'Lateral 2'.
        '''

        content_label_2 = Label(
            text=content_text_2,
            font_name="roboto_titulo",
            font_size=sp(20),
            size_hint_y=None,
            markup=True,
            color=(1, 1, 1, 1),
            text_size=(dp(300), None),
            halign='justify',
            valign='top'
        )
        content_label_2.bind(texture_size=content_label_2.setter('size'))
        content_layout.add_widget(content_label_2)

        scroll_view.add_widget(content_layout)
        layout.add_widget(scroll_view)

        self.add_widget(layout)

class ModelBScreen(Screen):
    def __init__(self, **kwargs):
        super(ModelBScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))

        title_label = Label(
            text='Modelo B',
            font_size=sp(30),
            font_name="roboto_titulo",
            size_hint_y=None,
            height=dp(40),
            color=(1, 1, 1, 1)
        )
        layout.add_widget(title_label)

        scroll_view = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        content_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10), size_hint_y=None)
        content_layout.bind(minimum_height=content_layout.setter('height'))

        content_text_1 = '''
        A continuación, se muestran imágenes del Modelo B. Si tu set de piezas se parece a las usadas en este modelo, selecciónalo para tus detecciones.
        '''
        content_label_1 = Label(
            text=content_text_1,
            font_name="roboto_titulo",
            font_size=sp(20),
            size_hint_y=None,
            markup=True,
            color=(1, 1, 1, 1),
            text_size=(dp(300), None),
            halign='justify',
            valign='top'
        )
        content_label_1.bind(texture_size=content_label_1.setter('size'))
        content_layout.add_widget(content_label_1)

        # Add images with captions
        image_1 = Image(
            source='assets/img/modelo_b_1.png',  # Update with the correct path to your image
            size_hint=(1, None),
            height=dp(200)
        )
        content_layout.add_widget(image_1)

        caption_1 = Label(
            text='Modelo B - Ejemplo 1',
            font_size=sp(16),
            size_hint_y=None,
            height=dp(30),
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle'
        )
        caption_1.bind(texture_size=caption_1.setter('size'))
        content_layout.add_widget(caption_1)

        image_2 = Image(
            source='assets/img/modelo_b_2.png',  # Update with the correct path to your image
            size_hint=(1, None),
            height=dp(200)
        )
        content_layout.add_widget(image_2)

        caption_2 = Label(
            text='Modelo B - Ejemplo 2',
            font_size=sp(16),
            size_hint_y=None,
            height=dp(30),
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle'
        )
        caption_2.bind(texture_size=caption_2.setter('size'))
        content_layout.add_widget(caption_2)

        image_3 = Image(
            source='assets/img/modelo_b_3.png',  # Update with the correct path to your image
            size_hint=(1, None),
            height=dp(200)
        )
        content_layout.add_widget(image_3)

        caption_3 = Label(
            text='Modelo B - Ejemplo 3',
            font_size=sp(16),
            size_hint_y=None,
            height=dp(30),
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle'
        )
        caption_3.bind(texture_size=caption_3.setter('size'))
        content_layout.add_widget(caption_3)



        content_text_2 = '''
        Como puedes observar, el ángulo usado es desde un punto de vista en picado. Por lo tanto, si utilizas este dataset, funcionará mejor desde un ángulo de vista 'Blanco' o 'Negro'.
        '''

        content_label_2 = Label(
            text=content_text_2,
            font_name="roboto_titulo",
            font_size=sp(20),
            size_hint_y=None,
            markup=True,
            color=(1, 1, 1, 1),
            text_size=(dp(300), None),
            halign='justify',
            valign='top'
        )
        content_label_2.bind(texture_size=content_label_2.setter('size'))
        content_layout.add_widget(content_label_2)

        scroll_view.add_widget(content_layout)
        layout.add_widget(scroll_view)

        self.add_widget(layout)

class BadResultScreen(Screen):
    def __init__(self, **kwargs):
        super(BadResultScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))

        title_label = Label(
            text='Resultados Incorrectos',
            font_size=sp(30),
            font_name="roboto_titulo",
            size_hint_y=None,
            height=dp(40),
            color=(1, 1, 1, 1)
        )
        layout.add_widget(title_label)

        scroll_view = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        content_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10), size_hint_y=None)
        content_layout.bind(minimum_height=content_layout.setter('height'))

        content_text_1 = '''
        Si después de varios intentos los resultados de detección no son precisos, la aplicación puede aún servir como una base útil para generar una posición que luego puedes editar para corregir los errores. A continuación, se detallan los pasos necesarios para editar los resultados.
        '''
        content_label_1 = Label(
            text=content_text_1,
            font_name="roboto_titulo",
            font_size=sp(20),
            size_hint_y=None,
            markup=True,
            color=(1, 1, 1, 1),
            text_size=(dp(300), None),
            halign='justify',
            valign='top'
        )
        content_label_1.bind(texture_size=content_label_1.setter('size'))
        content_layout.add_widget(content_label_1)

        # Add labels and images with captions
        step_1_text = '''
        Primero, obtendremos la posición detectada en Lichess, aunque no sea completamente correcta. El primer paso es hacer clic en el menú. La interfaz puede variar ligeramente dependiendo del dispositivo.
        '''
        step_1_label = Label(
            text=step_1_text,
            font_name="roboto_titulo",
            font_size=sp(20),
            size_hint_y=None,
            markup=True,
            color=(1, 1, 1, 1),
            text_size=(dp(300), None),
            halign='justify',
            valign='top'
        )
        step_1_label.bind(texture_size=step_1_label.setter('size'))
        content_layout.add_widget(step_1_label)

        image_1 = Image(
            source='assets/img/guia-1.jpeg',  # Update with the correct path to your image
            size_hint=(1, None),
            height=dp(200)
        )
        content_layout.add_widget(image_1)

        caption_1 = Label(
            text='Posición en Lichess',
            font_size=sp(16),
            size_hint_y=None,
            height=dp(30),
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle'
        )
        caption_1.bind(texture_size=caption_1.setter('size'))
        content_layout.add_widget(caption_1)

        step_2_text = '''
        A continuación, haz clic en el editor del tablero, lo cual abrirá una pantalla donde podrás ajustar la posición.
        '''

        step_2_label = Label(
            text=step_2_text,
            font_name="roboto_titulo",
            font_size=sp(20),
            size_hint_y=None,
            markup=True,
            color=(1, 1, 1, 1),
            text_size=(dp(300), None),
            halign='justify',
            valign='top'
        )
        step_2_label.bind(texture_size=step_2_label.setter('size'))
        content_layout.add_widget(step_2_label)

        image_2 = Image(
            source='assets/img/guia-2.jpeg',  # Update with the correct path to your image
            size_hint=(1, None),
            height=dp(200)
        )
        content_layout.add_widget(image_2)

        caption_2 = Label(
            text='Abrir el menú',
            font_size=sp(16),
            size_hint_y=None,
            height=dp(30),
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle'
        )
        caption_2.bind(texture_size=caption_2.setter('size'))
        content_layout.add_widget(caption_2)

        step_3_text = '''
        Por último, en la pantalla del editor, una vez que hayas realizado los cambios necesarios, haz clic en el icono correspondiente para volver al análisis.
        '''
        step_3_label = Label(
            text=step_3_text,
            font_name="roboto_titulo",
            font_size=sp(20),
            size_hint_y=None,
            markup=True,
            color=(1, 1, 1, 1),
            text_size=(dp(300), None),
            halign='justify',
            valign='top'
        )
        step_3_label.bind(texture_size=step_3_label.setter('size'))
        content_layout.add_widget(step_3_label)

        image_3 = Image(
            source='assets/img/guia-3.jpeg',  # Update with the correct path to your image
            size_hint=(1, None),
            height=dp(200)
        )
        content_layout.add_widget(image_3)

        caption_3 = Label(
            text='Editor de tablero',
            font_size=sp(16),
            size_hint_y=None,
            height=dp(30),
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle'
        )
        caption_3.bind(texture_size=caption_3.setter('size'))
        content_layout.add_widget(caption_3)

        scroll_view.add_widget(content_layout)
        layout.add_widget(scroll_view)

        self.add_widget(layout)

class PositionChoiceScreen(Screen):
    def __init__(self, **kwargs):
        super(PositionChoiceScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))

        img = Image(source='assets/img/camera_icon.png', keep_ratio=True, allow_stretch=True, size_hint=(1, 0.6))
        layout.add_widget(img)

        self.btn_camera = Factory.RoundedButton(text="Hacer foto", size_hint=(1, 0.1))
        self.btn_camera.bind(on_press=self.open_camera)
        layout.add_widget(self.btn_camera)

        self.btn_gallery = Factory.RoundedButton(text="Abrir galeria", size_hint=(1, 0.1))
        self.btn_gallery.bind(on_press=self.open_gallery)
        layout.add_widget(self.btn_gallery)

        self.add_widget(layout)

    def go_to_image_details(self, instance):
        self.manager.transition.direction = 'left'
        self.manager.current = 'image_detail'

    def on_button_press(self, instance):
        print("The button was clicked.")

    def open_camera(self, instance):

        self.loading_popup = LoadingPopup()
        self.loading_popup.open()
        Clock.schedule_once(self.start_open_camera)

    
    def start_open_camera(self,instance):
        self.manager.transition.direction = 'left'
        self.manager.current = 'photo_screen'
        self.loading_popup.dismiss()


    def open_gallery(self, instance=None):
        current_dir = os.getcwd()
        path_to_gallery = storagepath.get_pictures_dir()

        filechooser.open_file(title="Pick an image...", filters=[("Images", "*.jpg", "*.jpeg", "*.png")], path=path_to_gallery, on_selection=self._on_file_selected)

        os.chdir(current_dir)

    def _on_file_selected(self, selection):
        if selection:
            selected_file_path = selection[0]
            Clock.schedule_once(lambda dt: self.select_image(selected_file_path))
        else:
            print("No file was selected.")

    def refresh_ui(self):
        Window.canvas.ask_update()
        for widget in self.walk(loopback=True):
            widget.canvas.ask_update()

    def save_image(self, image_path):
        image = cv2.imread(image_path)
        if image is not None:
            save_path = 'saved_image.jpg'
            cv2.imwrite(save_path, image)
            print(f"Image saved successfully at {save_path}")
        else:
            print("Failed to read the image from selected file.")
    
    def select_image(self, posicion):
        if self.manager:
            if self.manager.has_screen('image_detail'):
                self.manager.remove_widget(self.manager.get_screen('image_detail'))
            detail_screen = ImageDetailScreen(image_path=posicion, name='image_detail')
            self.manager.transition = SlideTransition(direction='left')
            self.manager.add_widget(detail_screen)
            self.manager.current = 'image_detail'
            self.manager.transition = SlideTransition()

class LoadingPopup(Popup):
    def __init__(self, **kwargs):
        super(LoadingPopup, self).__init__(**kwargs)
        self.title = '   Cargando el modelo'
        self.title_size = '20sp'
        self.title_color = (1, 1, 1, 1)  # Blanco
        self.size_hint = (0.7, 0.2)
        self.size = (400, 200)  # Tamaño moderado para un diseño más centrado
        self.auto_dismiss = False

        # Ajustes para un fondo oscuro y opaco
        self.background_color = (0.1, 0.1, 0.1, 0.9)  # Fondo casi negro con alta opacidad
        self.separator_color = (0.8, 0.8, 0.8, 1)  # Gris claro

        # Crear y configurar el label para mostrar el mensaje de carga
        self.label = Label(
            text="Por favor, espere...",
            font_size='18sp',
            color=(0.8, 0.8, 0.8, 1),  # Gris claro
            size_hint_y=None,
            height=50,  # Altura del Label para asegurar espacio vertical adecuado
            text_size=(self.size[0], None),  # Configurar el tamaño del texto para permitir centrado
            valign='middle',  # Centrar verticalmente
            halign='center'  # Centrar horizontalmente
        )
        self.content = self.label
        self.label.bind(size=self.label.setter('text_size'))  # Asegurarse de que el tamaño del texto se ajuste con el tamaño del label

class LoadingPopup2(Popup):
    def __init__(self, **kwargs):
        super(LoadingPopup2, self).__init__(**kwargs)
        self.title = '         Escaneando ...'
        self.title_size = '20sp'
        self.title_color = (1, 1, 1, 1)  # Blanco
        self.size_hint = (0.7, 0.2)
        self.size = (400, 200)  # Tamaño moderado para un diseño más centrado
        self.auto_dismiss = False

        # Ajustes para un fondo oscuro y opaco
        self.background_color = (0.1, 0.1, 0.1, 0.9)  # Fondo casi negro con alta opacidad
        self.separator_color = (0.8, 0.8, 0.8, 1)  # Gris claro

        # Crear y configurar el label para mostrar el mensaje de carga
        self.label = Label(
            text="Por favor, espere...",
            font_size='18sp',
            color=(0.8, 0.8, 0.8, 1),  # Gris claro
            size_hint_y=None,
            height=50,  # Altura del Label para asegurar espacio vertical adecuado
            text_size=(self.size[0], None),  # Configurar el tamaño del texto para permitir centrado
            valign='middle',  # Centrar verticalmente
            halign='center'  # Centrar horizontalmente
        )
        self.content = self.label
        self.label.bind(size=self.label.setter('text_size'))  # Asegurarse de que el tamaño del texto se ajuste con el tamaño del label

class ChessBoard(GridLayout):
    def __init__(self, fen, **kwargs):
        super().__init__(**kwargs)
        self.cols = 8
        self.rows = 8
        self.fen = fen
        self.size_hint = (1, 1)
        self.setup_board(fen)

    def setup_board(self, fen):
        self.clear_widgets()  # Limpia el tablero antes de configurarlo de nuevo
        self.update_board(fen)

    def update_board(self, fen):
        """Actualiza el tablero con un nuevo FEN."""
        self.clear_widgets()  # Asegura eliminar todos los widgets existentes
        self.fen = fen
        rows = self.fen.split(" ")[0].split("/")
        board = [self.fen_row_to_pieces(row) for row in rows]
        for row_index, row in enumerate(board):
            for col_index, piece in enumerate(row):
                light_color = [240/255, 218/255, 181/255, 1]
                dark_color = [181/255, 135/255, 99/255, 1]
                color = light_color if (row_index + col_index) % 2 == 0 else dark_color
                box = MDBoxLayout(md_bg_color=color, size_hint=(1, 1))
                if piece:
                    prefix = 'w_' if piece.isupper() else 'b_'
                    img_path = f'chess_pieces/{prefix}{piece.lower()}.png'
                    image = Image(source=img_path, allow_stretch=True, keep_ratio=False)
                    box.add_widget(image)
                self.add_widget(box)

    def fen_row_to_pieces(self, fen_row):
        result = []
        for char in fen_row:
            if char.isdigit():
                result.extend([""] * int(char))
            else:
                result.append(char)
        return result





    def save_frame(self, instance=None):
        cam = self.camera
        image_object = cam.export_as_image(scale=round((400 / int(cam.height)), 2))
        w, h = image_object._texture.size
        frame = np.frombuffer(image_object._texture.pixels, 'uint8').reshape(h, w, 4)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)

        filename = f"frame_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        cv2.imwrite(filename, frame)
        print(f"Saved frame as {filename}")

class BaseCameraScreen(Screen):
    camera_instance = None

    def __init__(self, **kwargs):
        super(BaseCameraScreen, self).__init__(**kwargs)

    def on_pre_enter(self, *args):
        if BaseCameraScreen.camera_instance is None:
            BaseCameraScreen.camera_instance = Camera(index=0, resolution=(640, 480), play=True)
            BaseCameraScreen.camera_instance.keep_ratio = True
            BaseCameraScreen.camera_instance.allow_stretch = True
            BaseCameraScreen.camera_instance.size_hint = (1, None)
            BaseCameraScreen.camera_instance.height = Window.width * (480 / 640)  # Mantiene la relación de aspecto 4:3
        if BaseCameraScreen.camera_instance.parent:
            BaseCameraScreen.camera_instance.parent.remove_widget(BaseCameraScreen.camera_instance)
        self.add_widgets()  # Añadir los widgets específicos de la pantalla hija
        BaseCameraScreen.camera_instance.play = True

    def on_pre_leave(self, *args):
        BaseCameraScreen.camera_instance.play = False
        Clock.schedule_once(self.remove_camera, 0.5)

    def remove_camera(self, dt):
        if BaseCameraScreen.camera_instance.parent:
            BaseCameraScreen.camera_instance.parent.remove_widget(BaseCameraScreen.camera_instance)

    def add_widgets(self):
        pass  # Este método será implementado por las clases hijas para añadir sus widgets específicos

class CustomMDFloatingActionButton(MDFloatingActionButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.elevation = 0

    def on_elevation(self, *args):
        # Override to prevent shadow/elevation
        pass

class AnalizarEnVivoScreen(BaseCameraScreen):
    def __init__(self, **kwargs):
        super(AnalizarEnVivoScreen, self).__init__(**kwargs)
        
        # FloatLayout para contener todo
        self.main_layout = FloatLayout()
        self.add_widget(self.main_layout)
        
        # BoxLayout con padding alrededor
        self.padded_layout = BoxLayout(
            orientation='vertical',
            padding=[dp(10), dp(10), dp(10), dp(10)]  # Padding: left, top, right, bottom
        )
        self.main_layout.add_widget(self.padded_layout)
        
        self.layout = BoxLayout(orientation='vertical')
        self.padded_layout.add_widget(self.layout)
        
        self.chessboard = Factory.ChessBoard("8/8/8/8/8/8/8/8")
        self.btn_capture_video = Factory.SquaredButton(text="Iniciar Análisis", size_hint=(1, 0.2))
        self.btn_capture_video.bind(on_press=self.toggle_auto_capture)
        self.config_button = Factory.SquaredButton(text='Configuración', size_hint=(1, 0.2))
        self.config_button.bind(on_press=self.open_config_popup)
        self.btn_escanear = Factory.SquaredButton(text='Lichess', size_hint=(1, 0.2))
        self.btn_escanear.bind(on_press=self.redirect_to_lichess)

        self.fen = '8/8/8/8/8/8/8/8'
        self.auto_capture_event = None
        self.camera_view = 'Lateral 1'
        self.player_turn = 'Blanco'
        self.model = 'Modelo A'

    def add_widgets(self):
        if BaseCameraScreen.camera_instance is None:
            BaseCameraScreen.camera_instance = Camera(index=0, resolution=(640, 480), play=True)
            BaseCameraScreen.camera_instance.keep_ratio = True
            BaseCameraScreen.camera_instance.allow_stretch = True
            BaseCameraScreen.camera_instance.size_hint = (1, None)
            BaseCameraScreen.camera_instance.height = Window.width * (480 / 640)  # Mantiene la relación de aspecto 4:3

        if BaseCameraScreen.camera_instance.parent:
            BaseCameraScreen.camera_instance.parent.remove_widget(BaseCameraScreen.camera_instance)
        if self.chessboard.parent:
            self.chessboard.parent.remove_widget(self.chessboard)
        if self.btn_capture_video.parent:
            self.btn_capture_video.parent.remove_widget(self.btn_capture_video)
        if self.config_button.parent:
            self.config_button.parent.remove_widget(self.config_button)
        if self.btn_escanear.parent:
            self.btn_escanear.parent.remove_widget(self.btn_escanear)

        self.layout.add_widget(BaseCameraScreen.camera_instance)
        self.layout.add_widget(self.chessboard)
        
        button_layout = GridLayout(cols=2, size_hint=(1, 0.2))

        button_layout.add_widget(self.config_button)
        button_layout.add_widget(self.btn_escanear)
        
        square_layout = BoxLayout(orientation='vertical', size_hint=(1,0.2))

        square_layout.add_widget(self.btn_capture_video)
        
        self.layout.add_widget(button_layout)
        self.layout.add_widget(square_layout)

    def on_pre_enter(self, *args):
        super(AnalizarEnVivoScreen, self).on_pre_enter(*args)
        self.reset_to_initial_layout()

    def on_leave(self, *args):
        if self.auto_capture_event:
            self.auto_capture_event.cancel()
            self.auto_capture_event = None

            self.btn_capture_video.text = "Iniciar Captura de Imágenes"

        BaseCameraScreen.camera_instance.play = False
        self.fen = '8/8/8/8/8/8/8/8'
        self.chessboard.update_board(self.fen)
        self.layout.clear_widgets()
        super(AnalizarEnVivoScreen, self).on_leave(*args)

    def reset_to_initial_layout(self):
        self.layout.clear_widgets()
        self.add_widgets()

    def go_back(self, instance=None):
        self.manager.transition.direction = 'right'
        self.manager.current = 'home_screen'

    def toggle_auto_capture(self, instance):
        if self.auto_capture_event:
            self.auto_capture_event.cancel()
            self.auto_capture_event = None
            self.btn_capture_video.text = "Iniciar Captura de Imágenes"
        else:
            self.auto_capture_event = Clock.schedule_interval(self.save_frame, 1)
            self.btn_capture_video.text = "Detener Captura de Imágenes"

    def open_config_popup(self, instance):
        popup = Factory.ConfigPopup()
        popup.open()
        popup.bind(on_dismiss=lambda *args: self.process_new_config(popup.get_configuration()))

    def process_new_config(self, config):
        if config:
            self.camera_view = config['view']
            self.player_turn = config['turn']
            print(f"Nueva configuración aplicada: Vista - {self.camera_view}, Turno - {self.player_turn}")

    def redirect_to_lichess(self, instance):
        print(f"Redirecting to Lichess with FEN: {self.fen}")
        url = f'https://lichess.org/analysis/{self.fen}'
        webbrowser.open(url)

    def save_frame(self, instance=None):
        try:
            cam = BaseCameraScreen.camera_instance
            image_object = cam.export_as_image(scale=round((400 / int(cam.height)), 2))
            w, h = image_object._texture.size
            frame = np.frombuffer(image_object._texture.pixels, dtype=np.uint8)
            frame = frame.reshape((h, w, 4))
            frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)

            self.fen = main(frame,self.camera_view,self.model)

            if self.player_turn.lower() == 'negro':
                fen_parts = self.fen.split(' ')
                fen_parts[1] = 'b'  # Cambia el turno a 'b' (negro)
                self.fen = ' '.join(fen_parts)

            if self.fen and "8/8/8/8/8/8/8/8" not in self.fen:
                print(self.fen)
                self.chessboard.update_board(self.fen)

        except Exception as e:
            print(f"Error al guardar el frame: {e}")

class FotoScreen(BaseCameraScreen):
    def __init__(self, **kwargs):
        super(FotoScreen, self).__init__(**kwargs)

        self.layout = FloatLayout()
        self.add_widget(self.layout)

        self.photo_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        self.photo_image = Image(size_hint=(1, 1))

        self.btn_capture_photo = CustomMDFloatingActionButton(
            icon="camera",
            size_hint=(None, None),
            size=("56dp", "56dp"),
            pos_hint={'center_x': 0.5, 'y': 0.05},
            md_bg_color=(0.086, 0.086, 0.086, 1),
        )
        self.btn_capture_photo.bind(on_release=self.save_frame)

        self.btn_goto_details = Factory.RoundedButton(text="Ver Detalles")
        self.btn_goto_details.bind(on_press=self.goto_image_details)

        self.btn_retake_photo = Factory.RoundedButton(text="Tomar Otra Foto")
        self.btn_retake_photo.bind(on_press=self.retake_photo)

    def add_widgets(self):
        BaseCameraScreen.camera_instance.pos_hint = {'center_x': 0.5, 'center_y': 0.55}
        self.layout.add_widget(BaseCameraScreen.camera_instance)
        if self.btn_capture_photo not in self.layout.children:
            self.layout.add_widget(self.btn_capture_photo)

    def on_pre_enter(self, *args):
        super(FotoScreen, self).on_pre_enter(*args)
        self.reset_to_initial_layout()

    def on_leave(self, *args):
        super(FotoScreen, self).on_leave(*args)

        BaseCameraScreen.camera_instance.play = False
        self.reset_to_initial_layout()

    def reset_to_initial_layout(self):
        self.layout.clear_widgets()
        self.layout.add_widget(BaseCameraScreen.camera_instance)
        self.layout.add_widget(self.btn_capture_photo)
        self.photo_image.source = ''

    def go_back(self, instance=None):
        self.manager.transition.direction = 'right'
        self.manager.current = 'home_screen'

    def save_frame(self, instance=None):
        try:
            os.makedirs('./test_images', exist_ok=True)
            cam = BaseCameraScreen.camera_instance
            image_object = cam.export_as_image(scale=round((400 / int(cam.height)), 2))
            w, h = image_object._texture.size
            frame = np.frombuffer(image_object._texture.pixels, dtype=np.uint8)
            frame = frame.reshape((h, w, 4))
            frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
            self.photo_filename = f"./test_images/frame_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            cv2.imwrite(self.photo_filename, frame)
            print(f"Saved frame as {self.photo_filename}")
            self.show_taken_photo(self.photo_filename)
        except Exception as e:
            print(f"Error al guardar el frame: {e}")

    def show_taken_photo(self, filename):
        self.photo_image.source = filename
        self.photo_layout.clear_widgets()
        self.photo_layout.add_widget(self.photo_image)
        self.photo_layout.add_widget(self.btn_goto_details)
        self.photo_layout.add_widget(self.btn_retake_photo)
        self.layout.clear_widgets()
        self.layout.add_widget(self.photo_layout)

    def goto_image_details(self, instance):
        self.select_image(self.photo_filename)

    def select_image(self, image_path):
        if self.manager:
            if self.manager.has_screen('image_detail'):
                self.manager.remove_widget(self.manager.get_screen('image_detail'))
            detail_screen = ImageDetailScreen(image_path=image_path, name='image_detail')
            self.manager.transition = SlideTransition(direction='left')
            self.manager.add_widget(detail_screen)
            self.manager.current = 'image_detail'
            self.manager.transition = SlideTransition()

    def retake_photo(self, instance=None):
        os.remove(self.photo_image.source)
        self.reset_to_initial_layout()

class PositionsScreen(Screen):
    def __init__(self, **kwargs):
        super(PositionsScreen, self).__init__(**kwargs)
        self.posiciones = crear_posiciones()  # Supongamos que esta función ya está definida

        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        layout.add_widget(Label(text='Registro de Posiciones', font_size=sp(30), font_name="roboto_titulo", size_hint_y=None, height=dp(60), color=(1, 1, 1, 1)))
        
        scroll_view = ScrollView(size_hint=(1, 0.8), do_scroll_x=False, do_scroll_y=True)
        grid = GridLayout(cols=3, spacing=dp(10), size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        for posicion in self.posiciones:
            btn = Button(size_hint_y=None, height=dp(120))
            btn.background_normal = posicion.imagen
            btn.background_down = posicion.imagen
            btn.border = (0, 0, 0, 0)  # Elimina el borde para mantener la imagen completa visible
            btn.bind(on_press=lambda instance, pos=posicion: self.select_image(pos.imagen))
            grid.add_widget(btn)

        scroll_view.add_widget(grid)
        layout.add_widget(scroll_view)

        self.add_widget(layout)

    def select_image(self, posicion):
        

        if self.manager:
            # Buscar si ya existe una pantalla de detalles y eliminarla primero
            if self.manager.has_screen('image_detail'):
                self.manager.remove_widget(self.manager.get_screen('image_detail'))
            detail_screen = ImageDetailScreen(image_path=posicion, name='image_detail')
            self.manager.transition = SlideTransition(direction='left')
            self.manager.add_widget(detail_screen)
            self.manager.current = 'image_detail'
            self.manager.transition = SlideTransition()

    def go_to_home(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = 'home_screen'

class ConfigPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(separator_height=0, **kwargs)
        self.size_hint = (0.8, 0.5)
        self.title = 'Configuración de Detección'
        self.title_size = '20sp'
        self.title_color = [0.9, 0.9, 0.9, 1]  # color claro para el título

        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(0))  # spacing reducido a 0

        with self.canvas.after:
            self.line_color = Color(0, 0, 0, 0)  # Hace la línea transparente
            self.rect = Rectangle()

        # Selector de punto de vista
        self.view_spinner = Spinner(
            text='Seleccione el punto de vista',
            values=('Blanco', 'Negro', 'Lateral 1','Lateral 2'),
            size_hint=(1, 0.25),
            background_color=(0.2, 0.2, 0.2, 1),
            color=(1, 1, 1, 1),  # Blanco
            font_name='roboto_normal'
        )
        self.add_widget_with_border(self.view_spinner, layout)

        # Selector de turno
        self.turn_spinner = Spinner(
            text='Seleccione quién mueve',
            values=('Blanco', 'Negro'),
            size_hint=(1, 0.25),
            background_color=(0.2, 0.2, 0.2, 1),
            color=(1, 1, 1, 1),  # Blanco
            font_name='roboto_normal'
        )
        self.add_widget_with_border(self.turn_spinner, layout)

        # Selector de modelo
        self.model_spinner = Spinner(
            text='Seleccione el modelo',
            values=('Modelo A', 'Modelo B'),
            size_hint=(1, 0.25),
            background_color=(0.2, 0.2, 0.2, 1),
            color=(1, 1, 1, 1),  # Blanco
            font_name='roboto_normal'
        )
        self.add_widget_with_border(self.model_spinner, layout)

        # Botón para guardar configuración
        save_btn = Factory.GrayRoundedButton(text='Guardar', size_hint=(1, 0.25))
        save_btn.bind(on_press=self.dismiss)  # Cierra el popup
        self.add_widget_with_border(save_btn, layout)

        self.add_widget(layout)

    def on_size(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def add_widget_with_border(self, widget, layout):
        with widget.canvas.before:
            Color(0.9, 0.9, 0.9, 0.2)  # Color del borde
            Rectangle(pos=widget.pos, size=widget.size)

        widget.bind(pos=self.update_rect, size=self.update_rect)
        layout.add_widget(widget)

    def update_rect(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0.9, 0.9, 0.9, 0.2)  # Color del borde
            Rectangle(pos=instance.pos, size=instance.size)

    def get_configuration(self):
        # Retorna el punto de vista actual, quién mueve y el modelo con valores por defecto si no se selecciona nada
        view = self.view_spinner.text if self.view_spinner.text != 'Seleccione el punto de vista' else 'Lateral 2'
        turn = self.turn_spinner.text if self.turn_spinner.text != 'Seleccione quién mueve' else 'Blanco'
        model = self.model_spinner.text if self.model_spinner.text != 'Seleccione el modelo' else 'Modelo A'
        return {
            'view': view,
            'turn': turn,
            'model': model
        }

class CustomPopup(Popup):
    def __init__(self, **kwargs):
        super(CustomPopup, self).__init__(**kwargs)
        self.title = ''  # Sin título
        self.title_size = 0  # Tamaño del título a 0
        self.background = ''  # Fondo transparente
        self.background_color = (0, 0, 0, 0)  # Color de fondo transparente
        self.separator_height = 0  # Altura del separador a 0 para eliminar la barra
        loading_image = Image(source='assets/gif/loading_gif.gif')

        self.add_widget(loading_image)

class ImageDetailScreen(Screen):
    def __init__(self, image_path, **kwargs):
        super(ImageDetailScreen, self).__init__(**kwargs)

        self.restore_focus()
        self.refresh_ui()

        self.camera_view = 'Lateral 1'
        self.player_turn = 'Blanco'
        self.model = 'Modelo A'

        self.image_path = image_path
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))

        # Mostrar la imagen seleccionada
        self.image = Image(source=self.image_path, size_hint=(1, 0.8))
        layout.add_widget(self.image)

        config_button = Factory.RoundedButton(text='Configurar Detección')
        config_button.bind(on_press=self.open_config_popup)
        layout.add_widget(config_button)

        btn_scan = Factory.RoundedButton(text="Escanear y analizar")
        btn_scan.bind(on_press=self.start_analysis)
        layout.add_widget(btn_scan)

        # Botón para iniciar el análisis

        self.loading_popup = LoadingPopup2()
        self.loading_popup.overlay_color = (0, 0, 0, 0.3)  # Un ligero tono oscuro para el overlay

        self.add_widget(layout)

    def open_config_popup(self, instance):
        popup = Factory.ConfigPopup()
        popup.open()
        popup.bind(on_dismiss=lambda *args: self.process_new_config(popup.get_configuration()))

    def process_new_config(self, config):
        if config:
            self.camera_view = config['view']
            self.player_turn = config['turn']
            self.model = config['model']
            print(f"Nueva configuración aplicada: Vista - {self.camera_view}, Turno - {self.player_turn}, Modelo - {self.model}")

    def restore_focus(self):
        if not Window.focus:
            Window.hide()
            Window.show()

    def refresh_ui(self):
        Window.canvas.ask_update()  # Solicita la actualización del canvas

    def start_analysis(self, instance):
        self.loading_popup.open()
        Clock.schedule_once(self.perform_analysis, 0.5)

    def perform_analysis(self, dt):
        print("Realizando análisis de la imagen")
        fen_result = main(self.image_path, self.camera_view, self.model)  # Supongamos que main ahora sólo necesita la ruta de la imagen


        if self.player_turn.lower() == 'negro':
            fen_parts = fen_result.split(' ')
            fen_parts[1] = 'b'  # Cambia el turno a 'b' (negro)
            fen_result = ' '.join(fen_parts)


        self.loading_popup.dismiss()
        self.redirect_to_lichess(fen_result)

    def redirect_to_lichess(self, fen):
        url = f'https://lichess.org/analysis/{fen}'
        webbrowser.open(url)

    def go_back(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = 'home_screen'

class LichessFENApp(MDApp):
    def build(self):
        self.manager = ScreenManager(transition=SlideTransition())
        self.manager.add_widget(HomeScreen(name='home_screen'))
        self.manager.add_widget(PositionsScreen(name='positions_screen'))
        self.manager.add_widget(AnalizarEnVivoScreen(name='live_analysis_screen'))
        self.manager.add_widget(FotoScreen(name='photo_screen'))
        self.manager.add_widget(PositionChoiceScreen(name='position_choice'))
        self.manager.add_widget(ImageDetailScreen(image_path='test_images/1.jpg', name='image_detail'))
        self.manager.add_widget(HelpScreen(name='help_screen'))
        self.manager.add_widget(HowToUseScreen(name='how_to_use_screen'))
        self.manager.add_widget(ModelosHelpScreen(name='modelos_help_screen'))
        self.manager.add_widget(BadResultScreen(name='contact_support_screen'))
        self.manager.add_widget(ModelAScreen(name='model_a_screen'))
        self.manager.add_widget(ModelBScreen(name='model_b_screen'))

        self.screen_history = ['home_screen']  # Initialize with home screen in history

        self.theme_cls.primary_palette = 'Blue'
        self.theme_cls.theme_style = 'Dark'
        Window.clearcolor = (0.12, 0.12, 0.12, 1)

        self.icon = 'assets/img/logo.jpg'
        self.title = "Chess"
        
        Window.bind(on_keyboard=self.on_back_button)  # Bind the back button event
        return self.manager

    def on_back_button(self, window, key, *args):
        if key == 27:  # Key code for the back button on Android
            current_screen = self.manager.current
            print(current_screen)
            if current_screen == 'home_screen':
                return False  # Allow the default behavior to exit the app
            elif current_screen in ['live_analysis_screen', 'position_choice', 'help_screen']:
                self.manager.transition.direction = 'right'  # Set transition direction to right
                self.manager.current = 'home_screen'
                return True  # Return True to indicate the event has been handled
            elif current_screen in  ['photo_screen','image_detail']:
                self.manager.transition.direction = 'right'  # Set transition direction to right
                self.manager.current = 'position_choice'
                return True  # Return True to indicate the event has been handled
            elif current_screen in  ['how_to_use_screen','modelos_help_screen','contact_support_screen']:
                self.manager.transition.direction = 'right'  # Set transition direction to right
                self.manager.current = 'help_screen'
                return True  # Return True to indicate the event has been handled
            elif current_screen in  ['model_a_screen','model_b_screen']:
                self.manager.transition.direction = 'right'  # Set transition direction to right
                self.manager.current = 'modelos_help_screen'
                return True  # Return True to indicate the event has been handled
            else:
                return False  # Allow default behavior for unhandled cases

    def on_stop(self):
        Window.unbind(on_keyboard=self.on_back_button)  # Unbind the event on app stop



if __name__ == '__main__':
    LichessFENApp().run()