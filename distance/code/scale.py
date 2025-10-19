import configparser
import platform
import re
import tkinter as tk
from tkinter import ttk

import cv2
import pyautogui


class ScaleWindow:
    """A GUI for setting the map scale."""

    def __init__(self, master):
        """Initializes the scale window."""
        self.master = master
        self.config = self.read_config("code/buttons.ini")
        self.resolution = self.config.get('resolution', '3')
        self.resolution_data = self.get_resolution_data()
        self.scale = self.load_scale()

        self.configure_styles()
        self.create_widgets()
        self.focus_game_window()

    def configure_styles(self):
        """Configures ttk styles for a modern look."""
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background="#2E2E2E")
        style.configure("TLabel", background="#2E2E2E", foreground="#FFFFFF", font=('Calibri', 12))
        style.configure("TEntry", fieldbackground="#3C3C3C", foreground="#FFFFFF", bordercolor="#555555",
                        insertbackground="white")
        style.configure("TButton", background="#007ACC", foreground="white", font=('Calibri', 10, 'bold'),
                        borderwidth=0)
        style.map("TButton", background=[('active', '#005f9e')])

    def read_config(self, filename):
        """Reads configuration from an INI file."""
        config = configparser.ConfigParser()
        config.read(filename, encoding='utf-8')
        return {
            'scale_x': config.get("Combinations", "scale_x", fallback='15'),
            'scale_y': config.get("Combinations", "scale_y", fallback='71'),
            'resolution': config.get("Combinations", "Resolution", fallback='3'),
        }

    def get_resolution_data(self):
        """Returns screenshot region data based on screen resolution."""
        resolution_map = {
            '0': [1034, 436, 329, 329], '1': [1054, 514, 384, 384], '2': [1234, 604, 444, 444],
            '3': [1462, 622, 456, 456], '4': [1462, 742, 456, 456], '5': [1955, 835, 605, 605],
            '6': [2835, 835, 605, 605], '7': [2940, 1260, 900, 900], '8': [3924, 1684, 1196, 1196],
        }
        return resolution_map.get(self.resolution, [1462, 622, 456, 456])

    def load_scale(self):
        """Loads the map scale from a text file."""
        try:
            with open('code/scale.txt', 'r') as f:
                return float(f.read().strip() or 5.0)
        except (FileNotFoundError, ValueError):
            return 5.0

    def save_scale(self):
        """Saves the map scale to a text file."""
        with open('code/scale.txt', 'w') as f:
            f.write(str(self.scale))

    def create_widgets(self):
        """Creates and places all widgets in the window."""
        self.master.geometry(f"220x80+{self.config['scale_x']}+{self.config['scale_y']}")
        self.master.overrideredirect(True)
        self.master.lift()
        self.master.wm_attributes("-topmost", True)
        self.master.configure(bg="#2E2E2E")
        if platform.system() != "Windows":
            self.master.wm_attributes("-alpha", 0.85)

        self.label = ttk.Label(self.master, text=f'{self.scale:.1f} px/m', font=('Calibri', 16, 'bold'))
        self.label.pack(pady=(5, 2))

        input_frame = ttk.Frame(self.master)
        input_frame.pack(pady=5)
        validate_cmd = (self.master.register(self.validate_input), "%P")
        self.entry = ttk.Entry(input_frame, width=6, font=('Calibri', 12), validate="key",
                               validatecommand=validate_cmd)
        self.entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(input_frame, text="Set Scale", command=self.calculate_scale).pack(side=tk.LEFT)
        ttk.Button(self.master, text="X", command=self.close, width=2).place(x=195, y=2)

    def calculate_scale(self):
        """Calculates and updates the map scale."""
        map_distance = self.entry.get()
        if not map_distance:
            return

        x, y, w, h = self.resolution_data
        pyautogui.screenshot('Map.png', region=(x, y, w, h))
        minimap_image = cv2.imread("Map.png")

        objBukv = {0: [1, 'a'], 1: [5, 'e'], 2: [7, 'g']}
        letters = {'a': "aletter.png", 'e': "eletter.png", 'g': "gletter.png"}
        letter_positions = []
        for i, (letter, filename) in enumerate(letters.items()):
            template = cv2.imread(f"../data/resolution_{self.resolution}/{filename}")
            res = cv2.matchTemplate(minimap_image, template, cv2.TM_CCOEFF_NORMED)
            _, _, _, top_left = cv2.minMaxLoc(res)
            letter_positions.append(top_left)

        arrOfBukv = [letter_positions[0], letter_positions[1], letter_positions[2]]
        centOfBukv = (arrOfBukv[0][0] + arrOfBukv[1][0] + arrOfBukv[2][0]) / 3
        maxError = 0
        maxIndex = 2
        for i in range(len(arrOfBukv)):
            delta = abs(centOfBukv - arrOfBukv[i][0])
            if delta > maxError:
                maxError = delta
                maxIndex = i
        newArrOfBukv = []
        for i in range(len(arrOfBukv)):
            if i != maxIndex:
                arr = [arrOfBukv[i][1], objBukv[i]]
                newArrOfBukv.append(arr)

        line = (newArrOfBukv[1][0] - newArrOfBukv[0][0]) / (newArrOfBukv[1][1][0] - newArrOfBukv[0][1][0])
        if line <= 0:
            self.label["text"] = f"Error"
            return
        scale = int(map_distance) / line
        if scale == 0 or scale > 99:
            self.label["text"] = f"Error"
            self.entry.delete(0, tk.END)
            return
        self.scale = scale
        self.label["text"] = f"{round(scale, 1)} px/m"
        self.entry.delete(0, tk.END)
        self.save_scale()

    def validate_input(self, new_value):
        """Validates that the input is a number up to 4 digits."""
        return re.match(r"^\d{0,4}$", new_value) is not None

    def focus_game_window(self):
        """Brings the War Thunder window to the foreground on Windows."""
        if platform.system() == "Windows":
            try:
                import win32gui
                win = win32gui.FindWindow(None, "War Thunder")
                if win:
                    win32gui.SetForegroundWindow(win)
            except ImportError:
                pass  # win32gui not on this system

    def close(self):
        """Closes the scale window."""
        self.focus_game_window()
        self.master.destroy()


def main():
    """Main function to create and run the scale window."""
    try:
        root = tk.Tk()
        ScaleWindow(root)
        root.mainloop()
    except Exception as e:
        with open('error.log', 'a') as f:
            f.write(f'\\n\\nError in scale window: {e}\\n')


if __name__ == "__main__":
    main()
