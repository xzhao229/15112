from kivy.app import App
from kivy.lang import Builder
import ageEstimation as predict
import ageProgression as ageprogression
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
import numpy as np
from kivy.uix.camera import Camera
import cv2
import tensorflow as tf
from kivy.clock import Clock


class ScreenManagement(ScreenManager):
    pass


class AgeScreen(Screen):
    def __init__(self, **kwargs):
        super(AgeScreen, self).__init__(**kwargs)
        self.image = Image(source='ageEst.jpg')
        self.add_widget(self.image)
        Clock.schedule_interval(self.update_pic, 1)

    def update_pic(self, dt):
        self.image.reload()


class CameraScreen(Screen):
    def capture(self):
        camera = self.ids['camera']
        camera.export_to_png("current_test/test_1.png")
        im = cv2.imread("current_test/test_1.png", cv2.IMREAD_UNCHANGED)
        y, x = im[:, :, 3].nonzero()  # get the nonzero alpha coordinates
        minx = np.min(x)
        miny = np.min(y)
        maxx = np.max(x)
        maxy = np.max(y)
        cropImg = im[miny:maxy, minx:maxx]
        cv2.imwrite("current_test/test_1.png", cropImg)
        test_result = predict.main()
        cv2.imwrite('ageEst.jpg', test_result)


    def ageProgress(self):
        ageprogression.tmp()
        return

class ProgressionScreen(Screen):
    def aging(self):
        camera = self.ids['camera']
        camera.export_to_png("aging_test/test.png")
        im = cv2.imread("aging_test/test.png", cv2.IMREAD_UNCHANGED)
        y, x = im[:, :, 3].nonzero()  # get the nonzero alpha coordinates
        minx = np.min(x)
        miny = np.min(y)
        maxx = np.max(x)
        maxy = np.max(y)
        cropImg = im[miny:maxy, minx:maxx]
        cv2.imwrite("aging_test/test.png", cropImg)


GUI = Builder.load_string('''

GridLayout:
    cols: 1
    ScreenManager:
        id: screen_manager
        CameraScreen:
            name: "camera_click_screen"
            id: camera_click_screen
        AgeScreen:
            name: "check_screen"
            id: check_screen
        ProgressionScreen:
            name: 'progression_screen'
            id: progression_screen

<CameraScreen>
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
        on_press:  
            root.capture()
            app.root.ids['screen_manager'].transition.direction = 'left'
            app.root.ids['screen_manager'].current = 'check_screen'
    Button:
        id:recap
        text:'Take Another One'
        font_size:24
        bold: True
        size: 250, 90
        size_hint: None, None
        pos:root.width - 250, 0
        on_press: 
            root.ageProgress()
            app.root.ids['screen_manager'].transition.direction = 'left'
            app.root.ids['screen_manager'].current = 'progression_screen'
    Camera:
        id: camera
        resolution: 800,680
        
<AgeScreen>:
    
    canvas.before:
        BorderImage:
            source: 'bgp.jpg'
            pos: self.pos
            size: self.size
    
    Button:
        text: "Retake Photo"
        font_size: 30
        size: 240, 90
        size_hint: None, None
        bold: True
        on_press:  
            app.root.ids['screen_manager'].transition.direction = 'right'
            app.root.ids['screen_manager'].current = 'camera_click_screen'

<ProgressionScreen>:
    Button:
        text: "Retake Photo"
        font_size: 30
        size: 240, 90
        size_hint: None, None
        bold: True
        on_press:  
            app.root.ids['screen_manager'].transition.direction = 'right'
            app.root.ids['screen_manager'].current = 'camera_click_screen'

''')


class MainApp(App):
    def build(self):

        return GUI


if __name__ == '__main__':
    MainApp().run()
