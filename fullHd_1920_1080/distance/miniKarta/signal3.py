#from pynput.keyboard import Listener
#from pynput.keyboard import Listener
from pynput import mouse
import traceback
#import pressKey
#import time
import configparser

def signal3(queue):

    try:   
        
        def read_config(name):
            config = configparser.ConfigParser()
            config.read(name)
            conf = []
            conf.append(config.get("Комбинации", "Замер дистанции мышь"))
            conf.append(config.get("Комбинации", "Выставка масштаба мышь"))
            return conf
        conf = read_config("кнопки")
        
        def on_click(x, y, button, pressed):
            try:

                if not pressed:
                    return
                if button.name ==  conf[0]:
                    queue.put("distance")
                elif button.name == conf[1]:
                    queue.put("scale")

            except Exception as e:
                file = open('error.log', 'a')
                file.write('\n\n')
                traceback.print_exc(file=file, chain=True)
                traceback.print_exc()
                file.close()      
        
        
        if conf[0] or conf[1]:
            with mouse.Listener(on_click=on_click) as listener:
                listener.join()
            
    except Exception as e:
        file = open('error.log', 'a')
        file.write('\n\n')
        traceback.print_exc(file=file, chain=True)
        traceback.print_exc()
        file.write(str(e))
        file.close()
