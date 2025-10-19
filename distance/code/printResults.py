import configparser
import platform
import tkinter as tk
from queue import Empty


class ResultsOverlay:
    """A transparent, click-through overlay for displaying results."""

    def __init__(self, queue):
        """Initializes the overlay window."""
        self.queue = queue
        self.config = self.read_config("code/buttons.ini")
        self.root = self.create_window()
        self.label1, self.label2 = self.create_labels()
        self.waiting1 = None
        self.waiting2 = None

        self.root.after(0, self.process_queue)
        self.root.mainloop()

    def read_config(self, filename):
        """Reads configuration from an INI file."""
        config = configparser.ConfigParser()
        config.read(filename, encoding='utf-8')
        return {
            'print_x': config.get("Combinations", "print_x", fallback='15'),
            'print_y': config.get("Combinations", "print_y", fallback='15'),
            'print_distance': config.get("Combinations", "print_distance", fallback='1'),
            'print_azimuth': config.get("Combinations", "print_azimuth", fallback='1'),
            'print_transparent': config.get("Combinations", "print_transparent", fallback='1'),
            'print_time': config.get("Combinations", "print_time", fallback='7'),
        }

    def create_window(self):
        """Creates the main Tkinter window."""
        root = tk.Tk()
        root.geometry(f"+{self.config['print_x']}+{self.config['print_y']}")
        root.overrideredirect(True)
        root.lift()
        root.wm_attributes("-topmost", True)

        if platform.system() == "Windows":
            self.setup_windows_specific_attributes(root)
        else:
            root.wm_attributes("-alpha", 0.7)

        root.configure(bg="#2E2E2E")
        return root

    def setup_windows_specific_attributes(self, root):
        """Sets up Windows-specific attributes for transparency and click-through."""
        is_transparent = self.config['print_transparent'] == '1'
        bg_color = '#1C1C1C' if is_transparent else '#2E2E2E'
        root.configure(bg=bg_color)
        root.wm_attributes("-disabled", True)
        if is_transparent:
            root.wm_attributes("-transparentcolor", bg_color)

        try:
            import win32api, win32con, pywintypes
            hwnd = pywintypes.HANDLE(int(root.frame(), 16))
            ex_style = win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TRANSPARENT
            win32api.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, ex_style)
        except (ImportError, NameError):
            pass  # Non-Windows or missing pywin32

    def create_labels(self):
        """Creates the labels for displaying text."""
        fg_color = "#FFFFFF"
        bg_color = self.root.cget('bg')
        font_style = ('Calibri', 18, 'bold')

        label1 = tk.Label(self.root, text='', font=font_style, fg=fg_color, bg=bg_color, padx=10, pady=5)
        label2 = tk.Label(self.root, text='', font=font_style, fg=fg_color, bg=bg_color, padx=10, pady=5)
        return label1, label2

    def process_queue(self):
        """Processes messages from the queue to update the overlay."""
        try:
            msg = self.queue.get_nowait()
            self.handle_message(msg)
        except Empty:
            pass
        finally:
            self.root.after(15, self.process_queue)

    def handle_message(self, msg):
        """Handles a single message from the queue."""
        msg_type = msg[0]
        if msg_type == 'clear':
            self.clear_labels()
        elif msg_type == 'printResults':
            self.display_results(msg[1], msg[2])
        elif msg_type in ('errorArrow', 'errorMarker'):
            error_messages = {'errorArrow': 'Player Not Found', 'errorMarker': 'Marker Not Found'}
            self.display_error(error_messages[msg_type])

    def clear_labels(self):
        """Hides the labels."""
        for widget in [self.waiting1, self.waiting2]:
            if widget:
                self.root.after_cancel(widget)
        self.label1.pack_forget()
        self.label2.pack_forget()

    def display_results(self, distance, angle):
        """Displays the distance and azimuth results."""
        text1 = f"Distance: {distance}m"
        text2 = f"Azimuth: {angle}°"
        display_time = int(float(self.config['print_time']) * 1000)

        if self.config['print_distance'] == "1":
            self.label1.config(text=text1)
            self.label1.pack(anchor="nw")
            self.waiting1 = self.root.after(display_time, self.label1.pack_forget)
        if self.config['print_azimuth'] == "1":
            self.label2.config(text=text2)
            self.label2.pack(anchor="nw")
            self.waiting2 = self.root.after(display_time, self.label2.pack_forget)

    def display_error(self, text):
        """Displays an error message."""
        self.label1.config(text=text)
        self.label1.pack(pady=5)
        self.waiting1 = self.root.after(int(float(self.config['print_time']) * 1000), self.label1.pack_forget)


def printResults(queue):
    """Initializes and runs the results overlay."""
    try:
        ResultsOverlay(queue)
    except Exception as e:
        with open('error.log', 'a') as f:
            f.write(f'\\n\\nError in printResults: {e}\\n')
