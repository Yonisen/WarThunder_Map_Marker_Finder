from tkinter import *
from tkinter import ttk
import re
import win32gui
from threading import Timer
import traceback
import configparser
import pyautogui
import cv2

try: 

    def read_config(name):
        config = configparser.ConfigParser()
        config.read(name, encoding='utf-8')
        conf = {}
        conf['scale_x'] = config.get("Combinations", "scale_x")
        conf['scale_y'] = config.get("Combinations", "scale_y")
        conf['resolution'] = config.get("Combinations", "Resolution")
        return conf
    conf = read_config("code/buttons.ini")
    resolution = conf['resolution']

    resolutionObject = {
        '0': [1034,436,329,329,329,329], #1366x768    #[x,y,w,h,size,sizeReal]
        '1': [1054,514,384,384,384,384], #1440x900
        '2': [1234,604,444,444,444,444], #1680x1050
        '3': [1462,622,456,456,456,456], #1920x1080
        #'3': [1034,436,329,329,329,329], #2560x1080
        '4': [1955,835,605,605,465,605], #2560x1440
        '5': [2835,835,605,605,465,605], #3440x1440
        '6': [2940,1260,900,900,480,900], #3840x2160
        '7': [3924,1684,1196,1196,460,1196], #5120x2280
    }
    
    resolutionX = resolutionObject[resolution][0]
    resolutionY = resolutionObject[resolution][1]
    resolutionW = resolutionObject[resolution][2]
    resolutionH = resolutionObject[resolution][3]
    ######################################################################
    #Создание окна масштаба

    file = open('code/scale.txt', 'r')
    scale = file.read()
    file.close()
    if scale == "" or scale == "0":
        scale = "5"
        file = open('code/scale.txt', 'w')
        file.write(scale)
        file.close()
    scale = round(float(scale), 1)   

    def get_text():
        try:
            res = entry.get()
            if res != "":
                print('')
                screen = pyautogui.screenshot('Map.png', region=(resolutionX, resolutionY, resolutionW, resolutionH))
                karta = cv2.imread("Map.png")
                
                objBukv = {
                    0: [1, 'a'],
                    1: [5, 'e'],
                    2: [7, 'g']
                }

                abukva = cv2.imread(f"../data/resolution_{resolution}/aletter.png")
                resAbukva = cv2.matchTemplate(karta,abukva,cv2.TM_CCOEFF_NORMED)
                a, b, d, top_left_a = cv2.minMaxLoc(resAbukva)
                print("лев_верх_угол_буква_a",top_left_a)

                ebukva = cv2.imread(f"../data/resolution_{resolution}/eletter.png")
                resEbukva = cv2.matchTemplate(karta,ebukva,cv2.TM_CCOEFF_NORMED)
                a, b, d, top_left_e = cv2.minMaxLoc(resEbukva)
                print("лев_верх_угол_буква_e",top_left_e)

                gbukva = cv2.imread(f"../data/resolution_{resolution}/gletter.png")
                resGbukva = cv2.matchTemplate(karta,gbukva,cv2.TM_CCOEFF_NORMED)
                a, b, d, top_left_g = cv2.minMaxLoc(resGbukva)
                print("лев_верх_угол_буква_g",top_left_g)
                
                arrOfBukv = [top_left_a, top_left_e, top_left_g]
                centOfBukv = (arrOfBukv[0][0] + arrOfBukv[1][0] + arrOfBukv[2][0])/3
                maxError = 0
                maxIndex = 2
                for i in range(len(arrOfBukv)):
                    delta = abs(centOfBukv-arrOfBukv[i][0])
                    if delta>maxError:
                        maxError = delta
                        maxIndex = i
                newArrOfBukv = []
                for i in range(len(arrOfBukv)):
                    if i != maxIndex:
                        arr = [arrOfBukv[i][1], objBukv[i]]
                        newArrOfBukv.append(arr)
               
                line = (newArrOfBukv[1][0]-newArrOfBukv[0][0])/(newArrOfBukv[1][1][0]-newArrOfBukv[0][1][0])
                print(f'для рассчета масштаба были взяты буквы {newArrOfBukv[0][1][1]} и {newArrOfBukv[1][1][1]}')
                if line <= 0:
                    label["text"] = f"ошибка"
                    print('не удалось распознать буквы на миникарте')
                    return 
                scale = int(res)/line
                print(f'масштаб карты {scale}')
                if scale == 0:
                    label["text"] = f"ошибка"
                    entry.delete(0, END)
                    return 
                if scale > 99:
                    label["text"] = f"ошибка"
                    print('не удалось распознать буквы на миникарте')
                    return  
                file = open('code/scale.txt', 'w')
                file.write(str(scale))
                file.close()
                label["text"] = f"{round(scale, 1)} пикс/м"     # получаем введенный текст
                entry.delete(0, END)
        except Exception as e:
            file = open('error.log', 'a')
            file.write('\n\n')
            traceback.print_exc(file=file, chain=True)
            traceback.print_exc()
            file.close()

    def close():
        selectWindow()
        quit()

    def validation(newval):
        try:
            return re.match("^\d{0,4}$", newval) is not None
        except Exception as e:
            file = open('error.log', 'a')
            file.write('\n\n')
            traceback.print_exc(file=file, chain=True)
            traceback.print_exc()
            file.close()           

    def selectWindow(event=1):
        try:
            toplist = []
            winlist = []
            def enum_callback(hwnd, results):
                winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

            win32gui.EnumWindows(enum_callback, toplist)
            wt = [(hwnd, title) for hwnd, title in winlist if 'war thunder' in title.lower()]
            # just grab the first window that matches
            if wt !=[]:
                wt = wt[0]
                # use the window handle to set focus
                win32gui.SetForegroundWindow(wt[0])  
        except Exception as e:
            file = open('error.log', 'a')
            file.write('\n\n')
            traceback.print_exc(file=file, chain=True)
            traceback.print_exc()
            file.close()                

    root = Tk()
    geometry = f"199x70+{conf['scale_x']}+{conf['scale_y']}"
    root.geometry(geometry) 
    check = (root.register(validation), "%P")
    entry = Entry(fg="yellow", bg="black", font=('Roboto','16'), width = 5, validate="key", validatecommand=check)
    entry.master.overrideredirect(True)
    entry.master.lift()
    entry.master.wm_attributes("-topmost", True)
    entry.place(x=22, y=38)

    btn = ttk.Button(text="Масштаб", command=get_text)
    btn.master.overrideredirect(True)
    btn.master.lift()
    btn.master.wm_attributes("-topmost", True)
    btn.place(x=97, y=40)

    btn1 = ttk.Button(text="X", command=close, width=3)
    btn1.master.overrideredirect(True)
    btn1.master.lift()
    btn1.master.wm_attributes("-topmost", True)
    btn1.place(x=169, y=3)

    label = Label(root, text=f'{scale} пикс/м', font=('Roboto','19'), fg='yellow', bg='brown')
    label.master.overrideredirect(True)
    label.master.lift()
    label.master.wm_attributes("-topmost", True)
    label.pack()

    timeout = 0
    t = Timer(timeout, selectWindow)
    t.start()    
    
    root.mainloop()
    
    ######################################################################
except Exception as e:
    file = open('error.log', 'a')
    file.write('\n\n')
    traceback.print_exc(file=file, chain=True)
    traceback.print_exc()
    file.close()