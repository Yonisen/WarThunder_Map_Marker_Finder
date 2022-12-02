#from pynput.keyboard import Listener
#from pynput.keyboard import Listener
from pynput.keyboard import Controller, GlobalHotKeys
import traceback
#import pressKey
#import time
import configparser

try:
    keyboard = Controller()
    
    def read_config(name):
        config = configparser.ConfigParser()
        config.read(name)
        conf = []
        conf.append(config.get("Комбинации", "Замер дистанции"))
        conf.append(config.get("Комбинации", "Выставка масштаба"))
        return conf
    conf = read_config("кнопки")
    
    def on_activate_t():
        try:

            file = open('signalDistance.txt', 'w')
            file.write("1")
            file.close()               

        except Exception as e:
            file = open('error.log', 'a')
            file.write('\n\n')
            traceback.print_exc(file=file, chain=True)
            traceback.print_exc()
            file.close()      
            
    def on_activate_cn():
        try:
         
            file = open('signalScale.txt', 'w')
            file.write("1")
            file.close()
        
        except Exception as e:
            file = open('error.log', 'a')
            file.write('\n\n')
            traceback.print_exc(file=file, chain=True)
            traceback.print_exc()
            file.write(str(e))
            file.close()     
    

    findDistance = conf[0]
    if findDistance == "":
        print("кнопка для замера дистанции не назначена\nбудет использована клавиша t")
        findDistance  = "t"
    setScaling = conf[1]
    if setScaling == "":
        print("кнопка для выставки масштаба не назначена\nбудет использована комбинация <ctrl>+n")
        setScaling  = "<ctrl>+n"
    
    with GlobalHotKeys({
        findDistance: on_activate_t,
        setScaling: on_activate_cn}) as h:
        h.join()
        
except Exception as e:
    file = open('error.log', 'a')
    file.write('\n\n')
    traceback.print_exc(file=file, chain=True)
    traceback.print_exc()
    file.write(str(e))
    file.close()
