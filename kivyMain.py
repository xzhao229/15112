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
import cv2



Builder.load_string('''
<BackPacitureLayout>
    canvas.before:
        BorderImage:
            # BorderImage behaves like the CSS BorderImage
            # border: 10, 10, 10, 10
            texture: self.background_image.texture
            pos: self.pos
            size: self.size
            
    
<RootWidget>
    BackPacitureLayout:
        # size_hint: .9, .9
        pos_hint: {'center_x': .45, 'center_y': .5}
        rows:1
    Label:
        text: "Mason can tell your age"
        text_size: self.width-20, self.height-20
        color: 0,0,0,1
        pos_hint: {'x':0.3, 'top':0.95}
        valign: 'top'
        
    Button:
        text: 'Test'
        text_size: self.width-20, self.height-20
        size: 75, 30
        size_hint: None, None
        haligh: 'left'
        pos_hint: {'x':0.45, 'top':0.1}

    
''')


class BackPacitureLayout(GridLayout):
    background_image = ObjectProperty(Image(source='bgp.jpg'))

class RootWidget(FloatLayout):
    pass

class MainApp(App):

    def build(self):
        temp = RootWidget()
        self.img1 = Image()
        temp.add_widget(self.img1)
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0 / 33.0)
        return temp

    def update(self, dt):
        # display image from cam in opencv window
        ret, frame = self.capture.read()
        # cv2.imshow("CV2 Image", frame)
        # convert it to texture
        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        # display image from the texture
        self.img1.texture = texture1

if __name__ == '__main__':
    MainApp().run()