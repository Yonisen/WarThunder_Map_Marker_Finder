"""
This script is used for testing mouse input.

It uses the pynput library to listen for mouse clicks and prints the name
of the button that was pressed.
"""
from pynput import mouse



def on_click(x, y, button, pressed):
    """
    Callback function for mouse clicks.

    This function is called when a mouse button is clicked, and it prints the
    name of the button that was pressed.

    Args:
        x (int): The x-coordinate of the mouse click.
        y (int): The y-coordinate of the mouse click.
        button (Button): The button that was clicked.
        pressed (bool): True if the button was pressed, False if it was
            released.
    """
    if not pressed:
        return
    print(button.name)





# Collect events until released
with mouse.Listener(
        on_click=on_click) as listener:
    listener.join()

# ...or, in a non-blocking fashion:
