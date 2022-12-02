#from pynput.keyboard import Listener
from pynput.keyboard import Listener
from pynput.keyboard import Key, Controller, GlobalHotKeys, HotKey
import traceback
import pressKey
import time
import configparser
import random

try:
    keyboard = Controller()
    
    def read_config(name):
        config = configparser.ConfigParser()
        config.read(name)
        conf = []
        conf.append(config.get("Комбинации", "Желтая метка"))
        conf.append(config.get("Комбинации", "Замер дистанции"))
        conf.append(config.get("Комбинации", "Выставка масштаба"))
        return conf
    conf = read_config("кнопки")
    
    def on_activate_CtrlN():
        try:

            file = open('signalDistance.txt', 'w')
            file.write("1")
            file.close()

            distComb = findDistance.split("+")  
            for i in distComb:
                
                keyboard.release(HotKey.parse(i)[0])
                time.sleep(random.uniform(0.05, 0.15))
                #time.sleep(random.uniform(3, 7))

            markCombo = mark.split("+")
            for i in markCombo:
                keyboard.press(HotKey.parse(i)[0]) 
                time.sleep(random.uniform(0.05, 0.15))
                #time.sleep(random.uniform(3, 7))
            for i in range(len(markCombo)):
                keyboard.release(HotKey.parse(markCombo[i])[0])
                if i != len(markCombo) - 1:
                    time.sleep(random.uniform(0.05, 0.15))                

        except Exception as e:
            file = open('error.log', 'a')
            file.write('\n\n')
            traceback.print_exc(file=file, chain=True)
            traceback.print_exc()
            file.write(str(e))
            file.close()      
            
    def on_activate_CtrlM():
        try:
         
            file = open('signalScale.txt', 'w')
            file.write("1")
            file.close()

            setCombo = setScaling.split("+")
            for i in range(len(setCombo)):
                keyboard.release(HotKey.parse(setCombo[i])[0])
                if i != len(setCombo) - 1:
                    time.sleep(random.uniform(0.05, 0.15))                
            
        
        except Exception as e:
            file = open('error.log', 'a')
            file.write('\n\n')
            traceback.print_exc(file=file, chain=True)
            traceback.print_exc()
            file.write(str(e))
            file.close()     
    
    mark = conf[0]
    if mark == "":
        print("кнопка для желтой метки не назначена\nбудет использована кнопка q")
        mark  = "q"
    findDistance = conf[1]
    if findDistance == "":
        print("кнопка для замера дистанции не назначена\nбудет использована комбинация <ctrl>+n")
        findDistance  = "<ctrl>+n"
    setScaling = conf[2]
    if setScaling == "":
        print("кнопка для выставки масштаба не назначена\nбудет использована комбинация <ctrl>+m")
        setScaling  = "<ctrl>+m"
    
    with GlobalHotKeys({
        findDistance: on_activate_CtrlN,
        setScaling: on_activate_CtrlM}) as h:
        h.join()
except Exception as e:
    file = open('error.log', 'a')
    file.write('\n\n')
    traceback.print_exc(file=file, chain=True)
    traceback.print_exc()
    file.write(str(e))
    file.close()
