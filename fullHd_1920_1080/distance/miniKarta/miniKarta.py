import torch
import time
import distanceFinder
from tkinter import *
from subprocess import Popen

print("Инициализация нейросетей")

#инициализация модели нейросети для поиска танка
modelTank = torch.hub.load('../yolo5', 'custom', '../yolo5/bestTank.pt', source='local')#classes="1"

#инициализация модели нейросети для поиска метки
modelMarker = torch.hub.load('../yolo5', 'custom', '../yolo5/bestMarker.pt', source='local')#classes="1"

#перевод моделей в режим процессора
#только если нет норм видеокарты
modelTank.cpu()
modelMarker.cpu()


#настройка модели танка
modelTank.conf = 0.15  # NMS confidence threshold отсев по точности первый
modelTank.iou = 0.45  # NMS IoU threshold второй, то есть то что больше 45% в теории пройдет
modelTank.agnostic = False  # NMS class-agnostic
modelTank.multi_label = False  # NMS multiple labels per box несколько лейблов одному объекту
modelTank.classes = [0,1]  # (optional list) filter by class, i.e. = [0, 15, 16] for COCO persons, cats and dogs
                     #номера каких классов оставить
modelTank.max_det = 1000  # maximum number of detections per image
modelTank.amp = False  # Automatic Mixed Precision (AMP) inference

#настройка модели маркера
modelMarker.conf = 0.15  # NMS confidence threshold отсев по точности первый
modelMarker.iou = 0.45  # NMS IoU threshold второй, то есть то что больше 45% в теории пройдет
modelMarker.agnostic = False  # NMS class-agnostic
modelMarker.multi_label = False  # NMS multiple labels per box несколько лейблов одному объекту
modelMarker.classes = [0]  # (optional list) filter by class, i.e. = [0, 15, 16] for COCO persons, cats and dogs
                     #номера каких классов оставить
modelMarker.max_det = 1000  # maximum number of detections per image
modelMarker.amp = False  # Automatic Mixed Precision (AMP) inference

#модели нейросетей готовы к работе

#root = Tk()
#root.geometry("175x80+15+15")
#label = Label(root, text=f'Дист:\nАзимут:', font=('Roboto','19'), fg='black', bg='yellow')
#label.master.overrideredirect(True)
#label.master.lift()
#label.master.wm_attributes("-topmost", True)
#label.master.wm_attributes("-disabled", True)
#label.master.wm_attributes("-transparentcolor", "white")
#label.pack()
#root.update()

#comand=["python", 'scale.py']
#Popen(comand)

print("\nПрограмма ожидает сочетания клавиш")

while True:
    file = open('signalDistance.txt', 'r')
    signalDistance = file.read()
    file.close()
    if signalDistance == "1":
        print("")
        distanceFinder.checkDistance(modelTank, modelMarker)
        file = open('signalDistance.txt', 'w')
        file.write("0")
        file.close()
        
    file = open('signalScale.txt', 'r')
    signalScale = file.read()
    file.close()
    if signalScale == "1":
        #print("")
        comand=["python", 'scale.py']
        Popen(comand)        
        file = open('signalScale.txt', 'w')
        file.write("0")
        file.close()    
    time.sleep(0.3)
