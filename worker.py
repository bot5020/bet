from unittest import result
import numpy as np
import cv2
import re
import pytesseract
from collections import Counter
import sqlite3

print("Загрузка каскада...")
cascade = cv2.CascadeClassifier("haarcascade_russian_plate_number.xml")
print("Каскад загружен!")

print("Инициализация Tessaract...")
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
tessdata_dir_config = '--tessdata-dir "C:\\Program Files\\Tesseract-OCR\\tessdata"'
print("Инициализация завершена!")

# Функция для отображения картинки

def img_show(img, detect = []):
    if list(detect):
        for (x, y, w, h) in detect:
            cv2.rectangle(img, (x, y), (x + w, y + h), (36, 255, 12), 2)
        cv2.imshow("1", img)
        cv2.waitKey(0)
    else:
        cv2.imshow("1", img)
    cv2.waitKey(0)


def database(car_number): # не используеться 
    try:
        connection = sqlite3.connect('table_kpp.db')
        cursor = connection.cursor()
        
        connection.commit()
        connection.close()
    except Exception as e:
        print(e)

def fixed_bugs(value):
    for i in (0, 4, 5):
        if value[i] == "0": value = f"{value[:i]}о{value[i + 1:]}"
    return value

# рассчет вероятности
def probability(number_base):
    result = dict()
    data = Counter(number_base)
    print(data)
    for i in data:
        five_six = i[1:4].count("5") + i[1:4].count("6")
        result[fixed_bugs(i)] = int((data[i] / len(number_base)) * 100 / (five_six ** 2 if five_six != 0 else 1))
    return result

# функция поворота номера
def rotation(img, angle):
    (h, w) = img.shape[:2]
    center = (int(w / 2), int(h / 2))
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1)
    return cv2.warpAffine(img, rotation_matrix, (w, h))

# Функция для исключения лишних символов
def extra_symbols(number):
    # Оставляем только цифры и буквы
    text = "".join([c for c in number.lower() if c.isalnum()])
    
    # Заменяем похожие элементы
    repl = {"б":"6", "э":"9", "д": "а", "з": "3", "о": "0"}
    for i in repl: text = text.replace(i, repl[i])

    # Находим подходящую подстроку для номера
    num = re.findall(r'[авекмнрстху780]\d{3}[авекмнрстху780]{2}\d{2,3}', text)
    return num

# Функция изменения размера для распознования
def resizing(img, height = 130):
    h, w = img.shape[:2]
    ratio = height / h
    dimension = (int(w * ratio), height)
    return cv2.resize(img, dimension)

# Функция детектирования номера - возращает кортеж из координат возможных номеров
def get_number(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    numbers = cascade.detectMultiScale(gray, 1.1, 4)

    return numbers

# Функция распознавания
def num_to_text(img, num):
    xx, yy, ww, hh = num
    img_show(img)
    # Привести картинку к серому, применить фильтры, обрезать
    img = resizing(img[yy:yy + hh, xx:xx + ww, :])

    result = np.zeros(img.shape, dtype = np.uint8)

    #blurDetect = cv2.Laplacian(img, cv2.CV_64F).var()
    #kernel = np.ones((2, 4), np.uint8) if blurDetect < 100 else np.ones((1, 1), np.uint8)
    kernel = np.ones((1, 1), np.uint8)
    plate = cv2.dilate(img, kernel, iterations = 2)
    plate = cv2.erode(plate, kernel, iterations = 1)
    plate_gray = cv2.cvtColor(plate,cv2.COLOR_BGR2GRAY)
    number_base = []
    for i in range(10, 201, 10):
        plate = 255 - cv2.threshold(plate_gray, i, 255, cv2.THRESH_BINARY)[1] # Играем значением

        extract = cv2.merge([plate, plate, plate])
        cnts = cv2.findContours(plate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
        for c in cnts:
            x, y, w, h = cv2.boundingRect(c)
            if 700 < w * h < 3000 and 0.2 <= w / h <= 1.1:
                result[y : y + h, x : x + w] = extract[y : y + h, x : x + w]

        #img_show(255 - result)
        data = pytesseract.image_to_string(255 - result, lang="rus", config ="--psm 6")
        # print("!", data)
        nums = extra_symbols(data)
        if nums: number_base.extend(nums)
        #print(number_base)
    
    # Вычисление вероятности
    #print(probability(number_base))
    return number_base#probability(number_base)
    #if number_base:
        #data = probability(number_base)
        
        #for j in data:
        #    print(f"[Номер]: {j}")
        #    print(f"[Вероятность]: {data[j]}%")

def recognizer(img):
    nums = get_number(img)
    print([num_to_text(img, num) for num in nums])
    return [num_to_text(img, num) for num in nums]