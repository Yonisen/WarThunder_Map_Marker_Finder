import keyboard

def on_key_press(event):
    print(f"Нажата клавиша: {event}")

keyboard.on_press(on_key_press)

keyboard.wait('esc') 