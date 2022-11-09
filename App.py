from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.core.window import Window

from datetime import datetime

from recognizer import info, img

#Window.fullscreen = True
Window.size = (920, 600)
# функция для получения видео
def get_img():
    video = img()
    return video

# функция для получения информации при помощи базы данных
def get_information():
    inf = info()
    dic = { # Надо переделать через sql 
        'к900хн123': tuple(['Мокеев', 'Степан', 'хз', 'секретик не скажу', 'машина польностью в хлам, торомзов нет как она вообще едет'])
    }
    return dic, inf

class MainPage(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Обновление информации 
        Clock.schedule_interval(self.update_time, 30.0 / 1)
        Clock.schedule_interval(self.update_video, 10.0 / 1)
        Clock.schedule_interval(self.update_information, 15.0 / 1)
        # Информация полученная через базу данных
    
    def update_time(self, interval):
        date = datetime.now()
        self.ids.date.text = f'{date.strftime("%H:%M, %B ")}{int(date.strftime("%d"))}{date.strftime(", %Y")}'

    def update_video(self, interval):
        print(get_img())

        #video = np.array(img(), dtype = np.uint8)  
        #print(video)
        #video = img()
        #save =  Image.img.save('video.png')
        #plt.imsave('C:/Users/Степанчик/Desktop/app_kv/video.png', np.array(img()))
        #plt.savefig('C:/Users/Степанчик/Desktop/app_kv/video.png')

        #self.ids.video.text = 'video.png'
    def update_information(self, interval):
        dic = get_information()[0]
        if dic:
            inf = tuple(get_information()[1][0])

            self.ids.name.text = dic[inf[0]][0]
            self.ids.surname.text = dic[inf[0]][1]
            self.ids.patronymic.text = dic[inf[0]][2]
            self.ids.phone.text = dic[inf[0]][3]
            self.ids.car.text = dic[inf[0]][4]
              
class MainApp(App):
    def build(self):
        return MainPage()

if __name__ == '__main__':
        MainApp().run()