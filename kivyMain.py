from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.camera import Camera
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import ageEstimation as predict
import ageProgression as ageprogression
import numpy as np
import cv2


# define variable age and globalized later
age = 0

# Screen Manager Class
class AppScreenManager(ScreenManager):
    pass

# Helper Screen Class
class HelperScreen(Screen):
    pass

# Load Screen Class
class LoadScreen(Screen):
    numFaces = NumericProperty(0)
    # get the image path and save it at local folder for age progression use
    def load(self,path):

        im = cv2.imread(path[0], cv2.IMREAD_UNCHANGED)
        y, x = im[:, :, -1].nonzero()  # get the nonzero alpha coordinates
        minx = np.min(x)
        miny = np.min(y)
        maxx = np.max(x)
        maxy = np.max(y)
        # crop image boundary(some images may have boundary
        cropImg = im[miny:maxy, minx:maxx]
        # write the cropped image
        cv2.imwrite("images/estimation_test/test_1.png", cropImg)
        test_result, current_age, self.numFaces = predict.main()

        # if face is found
        if current_age != -1:
            self.test_age = int(current_age)
            self.manager.get_screen('check_screen').test_age = int(current_age)
            new_label = 'You look like ' + str(int(current_age)) + ' years old!'
            new_label_progres = 'This is what your look at age of ' + str(int(current_age)+ 4)
            self.manager.get_screen('progression_screen').message = new_label_progres
            self.manager.get_screen('check_screen').message = new_label
            # save age estimation result
            cv2.imwrite('images/estimation_results/ageEst.jpg', test_result)
            self.manager.current = 'check_screen'
        # face not found
        else:
            # stay at camera_click_screen
            app = App.get_running_app()
            app.root.ids['screen_manager'].current = "LoadScreen"

            # get the popup message to retest
            popup = Popup(title='No Face Detected, Please Try Again.',
                          content=Label(text='Click Anywhere To Close', font_name='comici'),
                          size_hint=(None, None), size=(280, 100))
            popup.open()
    # age progression function
    def ageProgress(self):
        if self.numFaces > 1:
            app = App.get_running_app()
            app.root.ids['screen_manager'].current = "check_screen"
            popup = Popup(title='More Than One Face Detected.',
                      content=Label(text='Please Try One Face for Progression\n'
                                         'Click Anywhere To Close', font_name='comici'),
                      size_hint=(None, None), size=(280, 100))
            popup.open()
        else:
            ageprogression.tmp()

# age screen
class AgeScreen(Screen):
    # message for updated label text
    message = StringProperty()
    test_age = NumericProperty(0)

    def __init__(self, **kwargs):
        super(AgeScreen, self).__init__(**kwargs)
        self.image = Image(source='images/estimation_results/ageEst.jpg')
        self.add_widget(self.image)
        Clock.schedule_interval(self.update_pic, 1)

    # update image
    def update_pic(self, dt):
        self.image.reload()

    # age progression function
    def ageProgress(self):
        ageprogression.tmp()
        return


class CameraScreen(Screen):
    # message for updated label age
    test_age = NumericProperty(0)
    numFaces = NumericProperty(0)
    # camera capture function
    def capture(self):
        # get camera ready
        camera = self.ids['camera']
        camera.export_to_png("images/estimation_test/test_1.png")
        im = cv2.imread("images/estimation_test/test_1.png", cv2.IMREAD_UNCHANGED)
        y, x = im[:, :, -1].nonzero()  # get the nonzero alpha coordinates
        minx = np.min(x)
        miny = np.min(y)
        maxx = np.max(x)
        maxy = np.max(y)
        # crop image boundary(some images may have boundary
        cropImg = im[miny:maxy, minx:maxx]
        cv2.imwrite("images/estimation_test/test_1.png", cropImg)
        test_result, current_age, self.numFaces = predict.main()
        print(self.numFaces)

        # if face is found
        if current_age != -1:
            self.test_age = int(current_age)
            self.manager.get_screen('check_screen').test_age = int(current_age)
            new_label = 'You look like ' + str(int(current_age)) + ' years old!'
            new_label_progres = 'This is what your look at age of ' + str(int(current_age)+ 4)
            self.manager.get_screen('progression_screen').message = new_label_progres
            self.manager.get_screen('check_screen').message = new_label
            cv2.imwrite('images/estimation_results/ageEst.jpg', test_result)
            self.manager.current = 'check_screen'
        # face not found
        else:
            # stay at camera_click_screen
            app = App.get_running_app()
            app.root.ids['screen_manager'].current = "camera_click_screen"
            # get the popup message to retest
            popup = Popup(title='No Faces Detected, Please Try Again.',
                          content=Label(text='Click Anywhere To Close',font_name = 'comici'),
                          size_hint=(None, None), size=(280, 100))
            popup.open()

    # age progression
    def ageProgress(self):
        if self.numFaces > 1:
            app = App.get_running_app()
            app.root.ids['screen_manager'].current = "check_screen"
            popup = Popup(title='More Than One Face Detected.',
                      content=Label(text='Please Try One Face for Progression\n'
                                         'Click Anywhere To Close', font_name='comici'),
                      size_hint=(None, None), size=(280, 100))
            popup.open()
        else:
            ageprogression.tmp()


# Age progression screen, enable check next age period, previous age period
class ProgressionScreen(Screen):

    # store message and predicted age for future display
    message = StringProperty()
    age = NumericProperty(0)

    # define times next age period or previous age period clicked and get image
    def __init__(self, **kwargs):
        super(ProgressionScreen, self).__init__(**kwargs)
        self.image = Image(source='images/progression_results/test_1_cropped.png_1.jpg')
        self.add_widget(self.image)
        Clock.schedule_interval(self.update_pic, 1)
        self.clickedTimes = 0
        self.currentAge = 0
    # update image for age progression
    def update_pic(self, dt):
        self.image.reload()

    # read the images and generate text label and estimated age for next time interval
    def nextAge(self):
        self.age = self.manager.get_screen('check_screen').test_age
        if self.clickedTimes <= 4:
            self.image.source = 'images/progression_results/test_1_cropped.png_'+str(self.clickedTimes)+'.jpg'
            self.currentAge = int(self.age) + 4 * self.clickedTimes
            self.message = 'This is what your look at age of ' + str(self.currentAge) + '!'

        else:
            self.clickedTimes = 4
            self.message = 'This is what your look at age of ' + str(self.currentAge) + '!'
            self.image.source = 'images/progression_results/test_1_cropped.png_' + str(self.clickedTimes) + '.jpg'

    # read the images and generate text label and estimated age for previous time interval
    def previousAge(self):
        self.age = self.manager.get_screen('check_screen').test_age
        if self.clickedTimes >= 1:
            self.currentAge = self.currentAge - 4
            self.message = 'This is what your look at age of ' + str(self.currentAge) + '!'
            self.image.source = 'images/progression_results/test_1_cropped.png_' + str(self.clickedTimes) + '.jpg'
        else:
            self.clickedTimes = 1
            self.message = 'This is what your look at age of ' + str(self.currentAge) + '!'
            self.image.source = 'images/progression_results/test_1_cropped.png_' + str(self.clickedTimes) + '.jpg'

# this is used for the screen, button, labels, images layout design
GUI = Builder.load_string('''

# screen manager, check screen name 
GridLayout:
    cols: 1
    AppScreenManager:
        id: screen_manager
        
        HelperScreen:
            name: 'HelperScreen'
            id: helper_screen
        LoadScreen:
            name: 'LoadScreen'
            id: load_screen
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
    # background picture
    canvas.before:
        BorderImage:
            source: 'images/bgp.jpg'
            pos: self.pos
            size: self.size
    #text label
    Label:
        text: "Age Prophet Tells Your Age From Your Look!"
        font_name: 'frfm721k'
        font_size : 28
        color: 0,0,0,1
        pos:0,370
        halign:'center'

    # two buttons
    Button:
        id:captureAndTest
        text: 'Test Your Age'
        font_size:24
        bold: True
        size: 200, 70
        size_hint: None, None
        font_name: 'comici'
        haligh: 'left'
        background_normal: 'images/buttonbgp.JPG'
        background_down: 'images/buttonbgp.JPG'
        color: 0,0,0,0.8
        pos:root.width - 200, 0
        on_press:  
            root.capture()
    Button: 
        id: mainScreenBut
        text: 'Back'
        bold: 'True'
        font_size: 24
        size: 200,70
        size_hint: None,None
        font_name: 'comici'
        color: 0,0,0,0.8
        # opacity: 1 if self.state == 'normal' else .5
            
        on_press:
            app.root.ids['screen_manager'].transition.direction = 'right'
            app.root.ids['screen_manager'].current = 'HelperScreen'
        background_normal: 'images/buttonbgp.JPG'
        background_down: 'images/buttonbgp.JPG'
    
    # camera, which will be activated automatically
    Camera:
        id: camera
        resolution: 800,680
        
<AgeScreen>:
    # background image
    canvas.before:
        BorderImage:
            source: 'images/bgp.jpg'
            pos: self.pos
            size: self.size
    # text labels
    Label:
        id:'ageScreenMessage'
        text: root.message
        font_name: 'frfm721k'
        font_size : 28
        color: 0,0,0,1
        pos:0,370
        halign:'center'
    
    # two buttons    
    Button:
        text: "Retake Photo"
        font_size: 24
        size: 220, 70
        size_hint: None, None
        bold: True
        background_normal: 'images/buttonbgp.JPG'
        background_down: 'images/buttonbgp.JPG'
        font_name: 'comici'
        color: 0,0,0,0.8
        
        on_press:  
            app.root.ids['screen_manager'].transition.direction = 'right'
            app.root.ids['screen_manager'].current = 'camera_click_screen'
    
    Button:
        id:recap
        text:'Age Progression'
        font_size:24
        bold: True
        size: 220, 70
        size_hint: None, None
        pos:root.width - 220, 0
        background_normal: 'images/buttonbgp.JPG'
        background_down: 'images/buttonbgp.JPG'
        font_name: 'comici'
        color: 0,0,0,0.8
        
        on_press: 
            root.ageProgress()
            app.root.ids['screen_manager'].transition.direction = 'left'
            app.root.ids['screen_manager'].current = 'progression_screen'

   
# the following two screen follows the same structure as previous 
<ProgressionScreen>:
    canvas.before:
        BorderImage:
            source: 'images/bgp.jpg'
            pos: self.pos
            size: self.size
    
    Label:
        id:'progressionScreenMessage'
        text: root.message
        font_name: 'frfm721k'
        font_size : 28
        color: 0,0,0,1
        pos:0,370
        halign:'center'
        
    Button:
        text: "Retake Photo"
        font_size: 24
        bold: True
        size: 200, 70
        size_hint: None, None  
        background_normal: 'images/buttonbgp.JPG'
        background_down: 'images/buttonbgp.JPG'
        color: 0,0,0,0.8
        font_name: 'comici'
        
        on_press:  
            app.root.ids['screen_manager'].transition.direction = 'right'
            app.root.ids['screen_manager'].current = 'camera_click_screen'
    
    Button:
        id:nextPro
        text:'4 Years Later'
        font_size:24
        bold: True
        size: 200, 70
        size_hint: None, None
        pos:root.width - 200, 0
        background_normal: 'images/buttonbgp.JPG'
        background_down: 'images/buttonbgp.JPG'
        color: 0,0,0,0.8
        font_name: 'comici'
        
        on_press: 
            root.clickedTimes += 1
            root.nextAge()
            
    Button:
        id:previousPro
        text:'4 Years Before'
        font_size:24
        bold:True
        size:200,70
        size_hint:None,None
        pos:root.width-400,0
        background_normal: 'images/buttonbgp.JPG'
        background_down: 'images/buttonbgp.JPG'
        color: 0,0,0,0.8
        font_name: 'comici'
        
        on_press:
            root.clickedTimes-=1
            root.previousAge()
            
            
            
<HelperScreen>:
    canvas.before:
        BorderImage:
            source: 'images/helperbgp.jpg'
            pos: self.pos
            size: self.size
    
    Label: 
        text: 'Age Prophet Instruction'
        color:0,0,0,1
        font_size: 36
        halign:'center'
        bold: True
        font_name: 'frfm721k'
        pos: 0,130
    
    Label:
        text: 'Age Prophet is dedicated to estimate your age from your face.\\n\
You could upload your photo from local or take a selfie.\\n\
Age Prophet shows the age of your face \\n\
Then, rogression function estimate and shows your look in next 4 years, \\n\
8 years, 12 years and 16 years!\\n Invite your friends and take a try!' 
        color: 0,0,0,1
        font_size: 26
        bold: True
        halign:'center'
        font_name: 'frfm721k'
        pos_hint: {'x':0, 'top':0.97}
    
    
    Button:
        text: "Load From Local"
        font_size: 24
        bold: True
        size: 220, 70
        size_hint: None, None  
        background_normal: 'images/buttonbgp.JPG'
        background_down: 'images/buttonbgp.JPG'
        color: 0,0,0,0.8
        font_name: 'comici'
        
        on_press:  
            app.root.ids['screen_manager'].transition.direction = 'right'
            app.root.ids['screen_manager'].current = 'LoadScreen'
    
    Button:
        text: "Camera Capture"
        font_size: 24
        bold: True
        size: 220, 70
        size_hint: None, None 
        pos:root.width-220,0 
        background_normal: 'images/buttonbgp.JPG'
        background_down: 'images/buttonbgp.JPG'
        color: 0,0,0,0.8
        font_name: 'comici'
        
        on_press:  
            app.root.ids['screen_manager'].transition.direction = 'right'
            app.root.ids['screen_manager'].current = 'camera_click_screen'
                  
            
            
<LoadScreen>:   
    # file chooser list 
    FileChooserListView
        id:fileChooser
        path:'~/'
    
    Button:
        id:select
        text: 'Select'
        bold: 'True'
        font_size: 24
        size: 200,70
        size_hint: None,None
        pos:root.width - 200, 0
        font_name: 'comici'
        color: 0,0,0,0.8
        
        on_press:
            root.load(fileChooser.selection)  
        background_normal: 'images/buttonbgp.JPG'
        background_down: 'images/buttonbgp.JPG'
    
    Button: 
        id: helper
        text: 'Back'
        bold: 'True'
        font_size: 24
        size: 200,70
        size_hint: None,None
        font_name: 'comici'
        color: 0,0,0,0.8
        opacity: 1 if self.state == 'normal' else .5
            
        on_press:
            app.root.ids['screen_manager'].transition.direction = 'left'
            app.root.ids['screen_manager'].current = 'HelperScreen'
        background_normal: 'images/buttonbgp.JPG'
        background_down: 'images/buttonbgp.JPG'       
            
''')

# main class
class MainApp(App):
    def build(self):
        return GUI


if __name__ == '__main__':
    MainApp().run()
