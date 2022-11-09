import cv2
from worker import recognizer

#-------------------
import matplotlib
matplotlib.use("TkAgg")
#-------------------

name = 'testik'

x, y, x2, y2 = 150, 150, 500, 300

def img():

    img = cv2.VideoCapture(0).read()[1]
    
    print('Загрузка завершнена ахахахахах')

    #cv2.rectangle(img, (x, y), (x2, y2), (255,198,255), 2)
    #cv2.imshow("frame", img) 
    if img is None:
        cv2.imwrite('save.jpg', img)
    else:
        print('камера не робит код фигня')
    # надо сделать мульпоточность для tmp с результатом

    return img#capture.read()[1]

'''

flag = True
while flag: # Получение видео  
    
    print(img)
    img = img[y + 2:y2 - 1, x + 2:x2 - 1]
    tmp = recognizer(img)
    flag = False
'''    
def info():
    tmp = recognizer(img())
    return tmp
