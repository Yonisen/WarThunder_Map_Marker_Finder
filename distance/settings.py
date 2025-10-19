import configparser
import re
import tkinter as tk
from contextlib import suppress
from tkinter import messagebox, ttk
import psutil


class SettingsWindow:
    """A GUI for configuring application settings."""

    def __init__(self, master):
        """Initializes the settings window."""
        self.master = master
        self.master.title("Settings")
        self.center_window(700, 550)
        self.master.configure(bg="#2E2E2E")
        self.style = self.configure_styles()

        self.config = self.read_config("code/buttons.ini")
        self.create_widgets()

    def center_window(self, width, height):
        """Centers the window on the screen."""
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.master.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

    def configure_styles(self):
        """Configures ttk styles for a modern look."""
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background="#2E2E2E")
        style.configure("TLabel", background="#2E2E2E", foreground="#FFFFFF", font=('Calibri', 12))
        style.configure("TEntry", fieldbackground="#3C3C3C", foreground="#FFFFFF", bordercolor="#555555",
                        insertbackground="white")
        style.configure("TRadiobutton", background="#2E2E2E", foreground="#FFFFFF", font=('Calibri', 11))
        style.map("TRadiobutton", background=[('active', '#3C3C3C')])
        style.configure("TCheckbutton", background="#2E2E2E", foreground="#FFFFFF", font=('Calibri', 11))
        style.map("TCheckbutton", background=[('active', '#3C3C3C')])
        style.configure("TButton", background="#007ACC", foreground="white", font=('Calibri', 12, 'bold'),
                        borderwidth=0)
        style.map("TButton", background=[('active', '#005f9e')])
        return style

    def create_widgets(self):
        """Creates and places all widgets in the window."""
        main_frame = ttk.Frame(self.master, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        hotkeys_frame = self.create_section_frame(main_frame, "Hotkeys")
        self.create_hotkey_settings(hotkeys_frame)

        display_frame = self.create_section_frame(main_frame, "Display")
        self.create_resolution_settings(display_frame)
        self.create_distance_window_settings(display_frame)
        self.create_scale_window_settings(display_frame)

        self.create_action_buttons(main_frame)

    def create_section_frame(self, parent, text):
        """Creates a labeled frame for a section of settings."""
        frame = ttk.LabelFrame(parent, text=text, style="TFrame")
        frame.pack(fill=tk.X, padx=5, pady=10, ipady=5)
        return frame

    def create_hotkey_settings(self, parent):
        """Creates widgets for hotkey configuration."""
        hotkey_labels = [
            "Distance Measurement:", "Scale Setting:",
            "Distance Measurement (Mouse):", "Scale Setting (Mouse):"
        ]
        self.hotkey_entries = []
        for i, text in enumerate(hotkey_labels):
            ttk.Label(parent, text=text).grid(row=i, column=0, sticky="w", padx=5, pady=5)
            entry = ttk.Entry(parent, width=25, font=('Calibri', 11))
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.hotkey_entries.append(entry)

        self.hotkey_entries[0].insert(0, self.config.get('distance_measurement', 't'))
        self.hotkey_entries[1].insert(0, self.config.get('scale_setting', '<ctrl>+n'))
        self.hotkey_entries[2].insert(0, self.config.get('distance_measurement_mouse', ''))
        self.hotkey_entries[3].insert(0, self.config.get('scale_setting_mouse', ''))

    def create_resolution_settings(self, parent):
        """Creates widgets for screen resolution selection."""
        res_frame = self.create_section_frame(parent, "Screen Resolution")
        self.resolution_var = tk.StringVar(value=self.config.get('resolution', '3'))
        resolutions = [
            ("1366x768", "0"), ("1440x900", "1"), ("1680x1050", "2"),
            ("1920x1080", "3"), ("1920x1200", "4"), ("2560x1440", "5"),
            ("3440x1440", "6"), ("3840x2160", "7"), ("5120x2280", "8")
        ]
        for i, (text, value) in enumerate(resolutions):
            ttk.Radiobutton(res_frame, text=text, value=value, variable=self.resolution_var).grid(
                row=i // 3, column=i % 3, sticky="w", padx=5)

    def create_distance_window_settings(self, parent):
        """Creates widgets for the distance overlay window settings."""
        dist_frame = self.create_section_frame(parent, "Distance Window")
        self.entry_print_x = self.create_labeled_entry(dist_frame, "X Position:", self.config.get('print_x', '15'))
        self.entry_print_y = self.create_labeled_entry(dist_frame, "Y Position:", self.config.get('print_y', '15'))
        self.entry_print_time = self.create_labeled_entry(dist_frame, "Display Time (s):",
                                                          self.config.get('print_time', '7'))

        self.print_distance = tk.IntVar(value=int(self.config.get('print_distance', 1)))
        self.print_azimuth = tk.IntVar(value=int(self.config.get('print_azimuth', 1)))
        self.print_transparent = tk.IntVar(value=int(self.config.get('print_transparent', 1)))

        ttk.Checkbutton(dist_frame, text="Show Distance", variable=self.print_distance).grid(row=3, column=0,
                                                                                             sticky="w", padx=5)
        ttk.Checkbutton(dist_frame, text="Show Azimuth", variable=self.print_azimuth).grid(row=3, column=1,
                                                                                           sticky="w", padx=5)
        ttk.Checkbutton(dist_frame, text="Transparent Background", variable=self.print_transparent).grid(
            row=4, columnspan=2, sticky="w", padx=5)

    def create_scale_window_settings(self, parent):
        """Creates widgets for the scale overlay window settings."""
        scale_frame = self.create_section_frame(parent, "Scale Window")
        self.entry_scale_x = self.create_labeled_entry(scale_frame, "X Position:", self.config.get('scale_x', '15'))
        self.entry_scale_y = self.create_labeled_entry(scale_frame, "Y Position:", self.config.get('scale_y', '71'))

    def create_action_buttons(self, parent):
        """Creates the 'Default', 'Apply', and 'Cancel' buttons."""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=10)
        ttk.Button(button_frame, text="Default", command=self.set_defaults, style="TButton").pack(side=tk.LEFT,
                                                                                                  padx=5)
        ttk.Button(button_frame, text="Apply", command=self.save_config, style="TButton").pack(side=tk.RIGHT,
                                                                                               padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.master.destroy, style="TButton").pack(side=tk.RIGHT)

    def create_labeled_entry(self, parent, text, default_value, row=None, col=0):
        """Helper to create a labeled entry widget."""
        if row is None:
            row = len(parent.grid_slaves())
        ttk.Label(parent, text=text).grid(row=row, column=col, sticky="w", padx=5, pady=2)
        entry = ttk.Entry(parent, width=10)
        entry.grid(row=row, column=col + 1, padx=5, pady=2)
        entry.insert(0, default_value)
        return entry

    def read_config(self, filename):
        """Reads configuration from an INI file."""
        config = configparser.ConfigParser()
        try:
            config.read(filename, encoding='utf-8')
            if "Combinations" not in config:
                config.add_section("Combinations")
        except FileNotFoundError:
            config.add_section("Combinations")
        return config['Combinations']

    def save_config(self):
        """Saves the current settings to the INI file."""
        config = configparser.ConfigParser()
        config.add_section("Combinations")
        config.set("Combinations", "Distance measurement", self.hotkey_entries[0].get())
        config.set("Combinations", "Scale setting", self.hotkey_entries[1].get())
        config.set("Combinations", "Distance measurement mouse", self.hotkey_entries[2].get())
        config.set("Combinations", "Scale setting mouse", self.hotkey_entries[3].get())
        config.set("Combinations", "Resolution", self.resolution_var.get())
        config.set("Combinations", "print_x", self.entry_print_x.get())
        config.set("Combinations", "print_y", self.entry_print_y.get())
        config.set("Combinations", "print_time", self.entry_print_time.get())
        config.set("Combinations", "print_distance", str(self.print_distance.get()))
        config.set("Combinations", "print_azimuth", str(self.print_azimuth.get()))
        config.set("Combinations", "print_transparent", str(self.print_transparent.get()))
        config.set("Combinations", "scale_x", self.entry_scale_x.get())
        config.set("Combinations", "scale_y", self.entry_scale_y.get())

        with open('code/buttons.ini', "w", encoding="utf-8") as f:
            config.write(f)

        self.terminate_child_processes()
        self.master.destroy()

    def set_defaults(self):
        """Resets all settings to their default values."""
        self.hotkey_entries[0].delete(0, tk.END)
        self.hotkey_entries[0].insert(0, 't')
        self.hotkey_entries[1].delete(0, tk.END)
        self.hotkey_entries[1].insert(0, '<ctrl>+n')
        self.hotkey_entries[2].delete(0, tk.END)
        self.hotkey_entries[3].delete(0, tk.END)

        self.resolution_var.set('3')
        self.print_distance.set(1)
        self.print_azimuth.set(1)
        self.print_transparent.set(1)

        self.entry_print_x.delete(0, tk.END)
        self.entry_print_x.insert(0, '15')
        self.entry_print_y.delete(0, tk.END)
        self.entry_print_y.insert(0, '15')
        self.entry_print_time.delete(0, tk.END)
        self.entry_print_time.insert(0, '7')
        self.entry_scale_x.delete(0, tk.END)
        self.entry_scale_x.insert(0, '15')
        self.entry_scale_y.delete(0, tk.END)
        self.entry_scale_y.insert(0, '71')

    def terminate_child_processes(self):
        """Terminates child processes related to the main application."""
        pids = []
        for pid_file in ['code/pid.txt', 'code/pid1.txt', 'code/pid3.txt', 'code/pid5.txt']:
            try:
                with open(pid_file, 'r') as f:
                    pids.append(int(f.read().strip()))
            except (FileNotFoundError, ValueError):
                continue

        parent_pid = pids[0] if pids else None
        if not parent_pid:
            return

        for pid in pids[1:]:
            with suppress(psutil.NoSuchProcess, ProcessLookupError):
                process = psutil.Process(pid)
                if process.name() == 'python.exe':
                    cmdline = process.cmdline()
                    for attr in cmdline:
                        if re.search(f'parent_pid={parent_pid}', attr):
                            process.terminate()
                            break


def main():
    """Main function to create and run the settings window."""
    try:
        root = tk.Tk()
        app = SettingsWindow(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
