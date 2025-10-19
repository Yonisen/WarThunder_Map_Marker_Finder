import configparser
import platform
import traceback
from pynput.keyboard import GlobalHotKeys


class HotkeyManager:
    """Manages global hotkeys for the application."""

    def __init__(self, queue):
        """Initializes the hotkey manager."""
        self.queue = queue
        self.config = self.read_config("code/buttons.ini")
        self.setup_hotkeys()

    def read_config(self, filename):
        """Reads hotkey configurations from an INI file."""
        config = configparser.ConfigParser()
        config.read(filename, encoding='utf-8')
        return {
            "distance": config.get("Combinations", "Distance measurement", fallback=None),
            "scale": config.get("Combinations", "Scale setting", fallback=None),
            "distance_mouse": config.get("Combinations", "Distance measurement mouse", fallback=None),
            "scale_mouse": config.get("Combinations", "Scale setting mouse", fallback=None),
        }

    def setup_hotkeys(self):
        """Sets up the global hotkeys based on the configuration."""
        if platform.system() == "Windows":
            try:
                import win32api
                win32api.LoadKeyboardLayout('00000409', 1)  # Set keyboard layout to English
            except ImportError:
                print("PyWin32 not installed. Hotkeys may not work as expected.")

        hotkey_map = {}
        if self.config["distance"]:
            hotkey_map[self.config["distance"]] = self.on_distance
        if self.config["scale"]:
            hotkey_map[self.config["scale"]] = self.on_scale

        if not hotkey_map:
            print("No keyboard hotkeys configured.")
            return

        listener = GlobalHotKeys(hotkey_map)
        listener.start()
        listener.join()

    def on_distance(self):
        """Callback for the distance measurement hotkey."""
        self.queue.put("distance")

    def on_scale(self):
        """Callback for the scale setting hotkey."""
        self.queue.put("scale")


def signal1(queue):
    """Initializes and runs the hotkey manager."""
    try:
        HotkeyManager(queue)
    except Exception as e:
        with open('error.log', 'a') as f:
            f.write(f'\\n\\nError in signal1: {e}\\n')
            traceback.print_exc(file=f, chain=True)
