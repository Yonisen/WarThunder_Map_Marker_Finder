import configparser
import traceback
from pynput import mouse


class MouseHotkeyManager:
    """Manages mouse hotkeys for the application."""

    def __init__(self, queue):
        """Initializes the mouse hotkey manager."""
        self.queue = queue
        self.config = self.read_config("code/buttons.ini")
        self.setup_mouse_listener()

    def read_config(self, filename):
        """Reads mouse hotkey configurations from an INI file."""
        config = configparser.ConfigParser()
        config.read(filename, encoding='utf-8')
        return {
            "distance": config.get("Combinations", "Distance measurement mouse", fallback=None),
            "scale": config.get("Combinations", "Scale setting mouse", fallback=None),
        }

    def setup_mouse_listener(self):
        """Sets up the global mouse listener."""
        if self.config["distance"] or self.config["scale"]:
            listener = mouse.Listener(on_click=self.on_click)
            listener.start()
            listener.join()
        else:
            print("No mouse hotkeys configured.")

    def on_click(self, x, y, button, pressed):
        """Callback for mouse click events."""
        if not pressed:
            return

        if button.name == self.config["distance"]:
            self.queue.put("distance")
        elif button.name == self.config["scale"]:
            self.queue.put("scale")


def signal3(queue):
    """Initializes and runs the mouse hotkey manager."""
    try:
        MouseHotkeyManager(queue)
    except Exception as e:
        with open('error.log', 'a') as f:
            f.write(f'\\n\\nError in signal3: {e}\\n')
            traceback.print_exc(file=f, chain=True)
