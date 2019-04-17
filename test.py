from kivy.app import App

from kivy.uix.scatter import Scatter
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import ScreenManager

# class ScreenRoot(Screen):   
#     pass
# 
class BGI(App):
    pass

class TestButton(App):
    pass
    
# class OtherScreen(Screen):   
#     pass


# class ScreenUpkeep(ScreenManager):    
#     pass



class TutorialApp(App):
    def build(self):
        layout = BoxLayout()
        btn1 = TestButton()
    # def build(self):
    #     return Builder.load_file("Tutorial.kv")



# class TutorialApp(App):
#     # def build(self):
#     #     return ScatterTextWidget()
#     # def build(self):
#     #     return tempWidget()
#     
#     def build(self):
#         layout = BoxLayout(orientation='vertical')
#         btn1 = Button(text='Hello',size = (20,20))
#         btn2 = Button(text='World')
#         wimg = Image(source='testigm.jpeg',pos_hint={'center_x':.5, 'center_y':.5},allow_stretch = True)
#         layout.add_widget(wimg)
#         layout.add_widget(btn1)
#         # layout.add_widget(btn2)
#         
#         return layout
if __name__ == "__main__":
    TutorialApp().run()