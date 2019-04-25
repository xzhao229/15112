from kivy.app import App
from kivy.lang import Builder
import ageEstimation as predict
import ageProgression as ageprogression
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
import numpy as np
from kivy.uix.camera import Camera
from kivy.clock import Clock
from kivy.uix.slider import Slider
import cv2
from kivy.properties import NumericProperty, StringProperty

age = 0

class AppScreenManager(ScreenManager):
    pass


class AgeScreen(Screen):
    message = StringProperty()
    test_age = NumericProperty(0)
    def __init__(self, **kwargs):
        super(AgeScreen, self).__init__(**kwargs)
        self.image = Image(source='images/estimation_results/ageEst.jpg')
        self.add_widget(self.image)
        Clock.schedule_interval(self.update_pic, 1)

    def update_pic(self, dt):
        self.image.reload()

    def ageProgress(self):
        ageprogression.tmp()
        return


class CameraScreen(Screen):
    test_age = NumericProperty(0)
    def capture(self):
        camera = self.ids['camera']
        camera.export_to_png("images/estimation_test/test_1.png")
        im = cv2.imread("images/estimation_test/test_1.png", cv2.IMREAD_UNCHANGED)
        y, x = im[:, :, 3].nonzero()  # get the nonzero alpha coordinates
        minx = np.min(x)
        miny = np.min(y)
        maxx = np.max(x)
        maxy = np.max(y)
        cropImg = im[miny:maxy, minx:maxx]
        cv2.imwrite("images/estimation_test/test_1.png", cropImg)
        test_result, current_age = predict.main()

        if current_age != -1:

            self.test_age = int(current_age)
            self.manager.get_screen('check_screen').test_age = int(current_age)
            new_label = 'You look like ' + str(int(current_age)) + ' years old.'
            new_label_progres = 'This is what your look at age of ' + str(int(current_age)+ 4)
            self.manager.get_screen('progression_screen').message = new_label_progres
            self.manager.get_screen('check_screen').message = new_label
            cv2.imwrite('images/estimation_results/ageEst.jpg', test_result)


    def ageProgress(self):
        ageprogression.tmp()
        return

class ProgressionScreen(Screen):

    message = StringProperty()
    age = NumericProperty(0)
    def __init__(self, **kwargs):
        super(ProgressionScreen, self).__init__(**kwargs)
        self.image = Image(source='images/progression_results/test_1_cropped.png_1.jpg')
        self.add_widget(self.image)
        Clock.schedule_interval(self.update_pic, 1)
        self.clickedTimes = 0
        self.currentAge = 0
    def update_pic(self, dt):
        self.image.reload()

    def nextAge(self):
        self.age = self.manager.get_screen('check_screen').test_age
        if self.clickedTimes <=4:
            self.image.source = 'images/progression_results/test_1_cropped.png_'+str(self.clickedTimes)+'.jpg'
            self.currentAge = int(self.age) + 4 * self.clickedTimes
            self.message = 'This is what your look at age of ' + str(self.currentAge)

        else:
            self.clickedTimes = 4
            self.message = 'This is what your look at age of ' + str(self.currentAge)
            self.image.source = 'images/progression_results/test_1_cropped.png_' + str(self.clickedTimes) + '.jpg'


    def previousAge(self):
        self.age = self.manager.get_screen('check_screen').test_age
        if self.clickedTimes >= 1:
            self.currentAge = self.currentAge-4
            self.message = 'This is what your look at age of ' + str(self.currentAge)
            self.image.source = 'images/progression_results/test_1_cropped.png_' + str(self.clickedTimes) + '.jpg'
        else:
            self.clickedTimes = 1
            self.message = 'This is what your look at age of ' + str(self.currentAge)
            self.image.source = 'images/progression_results/test_1_cropped.png_' + str(self.clickedTimes) + '.jpg'

GUI = Builder.load_string('''

GridLayout:
    cols: 1
    AppScreenManager:
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
            source: 'images/bgp.jpg'
            pos: self.pos
            size: self.size

    Label:
        text: "Age Prophet Tell Your Age From Your Look"
        text_size: self.width-20, self.height-30
        font_size : 28
        color: 0,0,0,1
        pos_hint: {'x':0.31, 'top':0.95}
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

    Camera:
        id: camera
        resolution: 800,680
        
<AgeScreen>:
    
    canvas.before:
        BorderImage:
            source: 'images/bgp.jpg'
            pos: self.pos
            size: self.size
    Label:
        id:'ageScreenMessage'
        text: root.message
        text_size: self.width-20, self.height-20
        font_size : 28
        color: 0,0,0,1
        pos_hint: {'x':0.35, 'top':0.95}
        valign: 'top'
    Button:
        text: "Retake Photo"
        font_size: 30
        size: 240, 90
        size_hint: None, None
        bold: True
        on_press:  
            app.root.ids['screen_manager'].transition.direction = 'right'
            app.root.ids['screen_manager'].current = 'camera_click_screen'
    
    Button:
        id:recap
        text:'Age Progression'
        font_size:24
        bold: True
        size: 250, 90
        size_hint: None, None
        pos:root.width - 250, 0
        on_press: 
            root.ageProgress()
            app.root.ids['screen_manager'].transition.direction = 'left'
            app.root.ids['screen_manager'].current = 'progression_screen'
    
    
<ProgressionScreen>:
    canvas.before:
        BorderImage:
            source: 'images/bgp.jpg'
            pos: self.pos
            size: self.size
    
    Label:
        id:'progressionScreenMessage'
        text: root.message
        text_size: self.width-20, self.height-20
        font_size : 28
        color: 0,0,0,1
        pos_hint: {'x':0.35, 'top':0.95}
        valign: 'top'
        
    Button:
        text: "Retake Photo"
        font_size: 24
        bold: True
        size: 250, 90
        size_hint: None, None  
        on_press:  
            app.root.ids['screen_manager'].transition.direction = 'right'
            app.root.ids['screen_manager'].current = 'camera_click_screen'
    
    Button:
        id:nextPro
        text:'4 Years Later'
        font_size:24
        bold: True
        size: 250, 90
        size_hint: None, None
        pos:root.width - 250, 0
        on_press: 
            root.clickedTimes += 1
            root.nextAge()
            
    Button:
        id:previousPro
        text:'4 Years Before'
        font_size:24
        bold:True
        size:250,90
        size_hint:None,None
        pos:root.width-500,0
        on_press:
            root.clickedTimes-=1
            root.previousAge()
''')


class MainApp(App):
    def build(self):
        return GUI


if __name__ == '__main__':
    MainApp().run()
