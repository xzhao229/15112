from kivy.app import App
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scatter import Scatter
from kivy.uix.image import Image
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
import cv2


Builder.load_string('''
    
<RootWidget>

    canvas.before:
        BorderImage:
            source: 'bgp.jpg'
            pos: self.pos
            size: self.size

    Label:
        text: "Mason can tell your age"
        text_size: self.width-20, self.height-20
        color: 0,0,0,1
        pos_hint: {'x':0.35, 'top':0.95}
        valign: 'top'
        
    Button:
        id:captureAndTest
        text: 'Test Your Age'
        font_size:24
        bold: True
        size: 240, 90
        size_hint: None, None
        haligh: 'left'
        pos_hint: {'x':0.349, 'top':0.2}
        on_release: camera.play = False
    Button:
        id:recap
        text:'Take Another One'
        font_size:24
        bold: True
        size: 250, 90
        size_hint: None, None
        pos_hint: {'x':0.505, 'top':0.2}
        on_release: camera.play = True
    
    Camera:
        id: camera
        resolution: 1080,1080

    
''')


class RootWidget(FloatLayout):
    def capture(self):
        pass

class MainApp(App):

    def build(self):
        temp = RootWidget()
        return temp




if __name__ == '__main__':
    MainApp().run()