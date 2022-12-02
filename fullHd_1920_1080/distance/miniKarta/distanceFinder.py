#from PIL import ImageGrab
#from PIL import Image
import cv2
import numpy as np
import math
from subprocess import Popen
import pyautogui

def checkDistance(modelTank, modelMarker):
  
        ######################################################################
        screen = pyautogui.screenshot('karta.png', region=(1462,622, 456, 456))
        #screenScale = ImageGrab.grab(bbox =(1745, 902, 1905, 1062))
        size = 456           
        #screen.save("karta.png")
        karta = cv2.imread("karta.png")
        #im1 = Image.fromarray(im1)
        #im1.save("karka.png")

        #screen = pyautogui.screenshot('karta.png', region=(1472,632, 448, 448))

        ######################################################################


        ####
        file = open('масштаб.txt', 'r')
        scale = file.read()
        file.close()
        if scale == "" or scale == "0":
            scale = "1"
            file = open('масштаб.txt', 'w')
            file.write(scale)
            file.close()
        scale = int(scale)
        #numberResults = modelNumber(screenScale, size=160)
        #print(numberResults.xyxy[0])
        #numberList = numberResults.xyxy[0].numpy().tolist()
        #if numberList == []:
        #    showErrorNumber(label, root)
        #    return
        #numberList.sort()
        #scale = ""
        #for i in numberList:
        #   scale += str(int(i[5]))
        #scale = int(scale)
        ###




        ######################################################################
        #Определяем позицию танка
        
        arrowResults = modelTank(screen, size)
        #print(arrowResults.xyxy[0])                            
        arrowsConfidences = arrowResults.xyxy[0][:, -2].numpy().tolist()        
        if arrowsConfidences == []:
            showErrorArrow(scale, screen)
            return
        arrowsCoords = arrowResults.xyxy[0][:, :-2].numpy()
        arrowIndex = 0
        arrowMaxConf = 0
        
        for i in range(len(arrowsConfidences)):
            if arrowsConfidences[i] > arrowMaxConf:
                arrowMaxConf = arrowsConfidences[i]
                arrowIndex = i       

        tankArrow = arrowsCoords[arrowIndex]
        #print(tankArrow)
        ###
        tankPosition = ((tankArrow[2]+tankArrow[0])/2, (tankArrow[3]+tankArrow[1])/2)
        #      xmin    ymin    xmax   ymax  confidence  class    name
        # 0  749.50   43.50  1148.0  704.5    0.874023      0   arrow
        ###

        print("Позиция танка",tankPosition)
        ######################################################################




        ######################################################################
        #Определяем позицию желтой метки

        #yellowMarker = cv2.imread("marker.png")#[..., ::-1]
        #resMarker = cv2.matchTemplate(karta,yellowMarker,cv2.TM_CCOEFF_NORMED)
        #a, b, d, top_left_marker = cv2.minMaxLoc(resMarker)
        #heightMarker, widthMarker, shit = yellowMarker.shape
        
        markerResults = modelMarker(screen, size)
        #print(markerResults.xyxy[0])                             
        markerConfidences = markerResults.xyxy[0][:, -2].numpy().tolist()        
        if markerConfidences == []:
            showErrorMarker(scale, screen)
            return
        markerCoords = markerResults.xyxy[0][:, :-2].numpy()
        markerIndex = 0
        markerMaxConf = 0
        
        for i in range(len(markerConfidences)):
            if markerConfidences[i] > markerMaxConf:
                markerMaxConf = markerConfidences[i]
                markerIndex = i       

        yellowMarker = markerCoords[markerIndex]        
        
        ###
        #markerPosition = (top_left_marker[0]+widthMarker/2, top_left_marker[1]+heightMarker/2)
        markerPosition = ((yellowMarker[2]+yellowMarker[0])/2, (yellowMarker[3]+yellowMarker[1])/2)
        ###

        print("Центр желтого маркера",markerPosition)
        ######################################################################




        #катеты по двум точкам
        katet1 = abs(tankPosition[0] - markerPosition[0])
        katet2 = abs(tankPosition[1] - markerPosition[1])


        ######################################################################
        #дистанция между двумя точками в пикселях
        gipotenuza = np.hypot(katet1, katet2)
        ######################################################################


        angel = 0

        if katet1==0 : #обходим деление на ноль
            angel = 90 #угол между двумя катетами
        else:
            angel = math.degrees(math.atan(katet2/katet1)) #тот же угол

        ######################################################################
        #получаем азимут
        if markerPosition[0]>=tankPosition[0] and markerPosition[1]<=tankPosition[1] :
            
            angel = 90-angel    
            
        elif markerPosition[0]>=tankPosition[0] and markerPosition[1]>tankPosition[1] :
            
            angel = 90+angel
            
        elif markerPosition[0]<tankPosition[0] and markerPosition[1]>=tankPosition[1] :
            
            angel = 270-angel
            
        elif markerPosition[0]<tankPosition[0] and markerPosition[1]<tankPosition[1] :
            
            angel = 270+angel
            
        #азимут найден
        ######################################################################





        ######################################################################
        #определяем длину единичного отрезка в пикселях
        #по сути тот отрезок, что улитка на миникарте помечает
        #но он всегда разный, поэтому я получил его из
        #взаимного расположения букв по краям миникарты

        ###буква A и буква E

        abukva = cv2.imread("abukva.png")
        resAbukva = cv2.matchTemplate(karta,abukva,cv2.TM_CCOEFF_NORMED)
        a, b, d, top_left_a = cv2.minMaxLoc(resAbukva)
        print("лев_верх_угол_буква_a",top_left_a)

        ebukva = cv2.imread("ebukva.png")
        resEbukva = cv2.matchTemplate(karta,ebukva,cv2.TM_CCOEFF_NORMED)
        a, b, d, top_left_e = cv2.minMaxLoc(resEbukva)
        print("лев_верх_угол_буква_e",top_left_e)
        ###


        
        line = (top_left_e[1] - top_left_a[1])/4
        if line == 0:
            showAError(scale)  
            return
        ######################################################################
        
        #получаем дистанцию в метрах
        distance = gipotenuza/line*scale
        print("азимут",angel)
        print("Дистанция",distance)
        

        #proc = subprocess.Popen(command, startupinfo=startupinfo)
        comand=["python", 'printResults.py', "true", f'{round(distance)}', f'{round(angel,1)}', f'{scale}']
        #Popen(comand, stdin=None, stdout=None, stderr=None, creationflags = 0x08000000)
        Popen(comand)
        #os.system(f'python printResults.py {round(distance)} {round(angel,1)}')
        #label['text'] = f'Дист: {round(distance)}\nАзимут: {round(angel,1)}'
        #if label['bg'] == "yellow":
        #    label['bg'] = "orange"
        #else:
        #    label['bg'] = "yellow"
        #root.update()
        ######################################################################
def showErrorArrow(scale, screen):
    file = open('shit_detection/tank/number.txt', 'r')
    number = file.read()
    if number == "":
        number = "0"
    number = int(number)
    file.close()
    file = open('shit_detection/tank/number.txt', 'w')    
    screen.save(f'shit_detection/tank/screen{number}.png')
    number+=1
    file.write(str(number))
    file.close()
    comand=["python", 'printResults.py', "errorArrow", f'{scale}']
    Popen(comand)
    #label['text'] = 'твой танк\nне найден'
    #if label['bg'] == "yellow":
    #    label['bg'] = "orange"
    #else:
    #    label['bg'] = "yellow"
    #root.update()

def showErrorMarker(scale, screen):
    file = open('shit_detection/marker/number.txt', 'r')
    number = file.read()
    if number == "":
        number = "0"
    number = int(number)
    file.close()
    file = open('shit_detection/marker/number.txt', 'w')    
    screen.save(f'shit_detection/marker/screen{number}.png')
    number+=1  
    file.write(str(number))
    file.close()
    comand=["python", 'printResults.py', "errorMarker", f'{scale}']
    Popen(comand)
    #label['text'] = 'метка\nне найдена'
    #if label['bg'] == "yellow":
    #    label['bg'] = "orange"
    #else:
    #    label['bg'] = "yellow"
    #root.update()
def showAError(scale):
    comand=["python", 'printResults.py', "AError", f'{scale}']
    Popen(comand)
#def showErrorNumber(label, root):
#    label['text'] = 'масштаб\nкарты\nне определен'
#    if label['bg'] == "yellow":
#        label['bg'] = "orange"
#    else:
#        label['bg'] = "yellow"
#    root.update()
