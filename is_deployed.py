"""
This module contains a GUI application that checks the status of a folder containing deployed files.
The application displays the status of the folder (deployed, deploying, or down) and the time since last status change.
The user can browse for the folder to check and the application will poll the folder every 5 seconds to update the status.

The application is written in Python 3.7 and uses the tkinter library for the GUI.

Author: Toni Heinänen
"""

from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import sys
import os
import glob
import json

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer


class StatusChecker:
    STATUS_FAILED = "[FAILED]"
    STATUS_DOWN = "[DOWN]"
    STATUS_DEPLOYED = "[DEPLOYED]"
    STATUS_DEPLOYING = "[DEPLOYING]"

    COLOR_RED = "red"
    COLOR_PINK = "pink"
    COLOR_LIGHT_GREEN = "light green"
    COLOR_YELLOW = "yellow"

    def __init__(self, path, filename):
        self.path = path
        self.filename = filename

    def check_status(self):
        status = self.STATUS_DOWN
        bg_color = self.COLOR_PINK
        time = ""

        if os.path.exists(self.path) and os.path.isdir(self.path):
            deployed_files = glob.glob(os.path.join(self.path, f"{self.filename}.deployed"))
            deploying_files = glob.glob(os.path.join(self.path, f"{self.filename}.isdeploying"))
            failed_files = glob.glob(os.path.join(self.path, f"{self.filename}.failed"))

            if deployed_files:
                status = self.STATUS_DEPLOYED
                bg_color = self.COLOR_LIGHT_GREEN
                time = self.get_latest_file_time(deployed_files)
            elif deploying_files:
                status = self.STATUS_DEPLOYING
                bg_color = self.COLOR_YELLOW
                time = self.get_latest_file_time(deploying_files)
            elif failed_files:
                status = self.STATUS_FAILED
                bg_color = self.COLOR_RED
                time = self.get_latest_file_time(failed_files)
            else:
                time = datetime.fromtimestamp(os.path.getctime(
                    self.path)).strftime('%Y-%m-%d %H:%M')

        history.add_status(status)


        return status, bg_color, time

    def get_latest_file_time(self, files):
        latest_file = max(files, key=os.path.getctime)
        return datetime.fromtimestamp(os.path.getctime(latest_file)).strftime('%Y-%m-%d %H:%M')


class IsDeployedApp(tk.Tk):
    TITLE = "Folderscanner (is_deployed?)"
    WINDOW_SIZE = "400x135"
    DEFAULT_FONT = "Sans Serif"
    DEFAULT_FONT_SIZE = 10
    DEFAULT_PADDING = (5, 5)

    POLL_INTERVAL = 5000
    DEFAULT_ENTRY_TEXT = "Path to jboss deployments folder"
    DEFAULT_FILENAME_TEXT = "Filename to scan for"
    INFO_TITLE = "Information about the app"
    INFO_TEXT = "Browse for the folder containing the deployed files\n" \
        "and enter the filename to scan for.\n\n" \
        "The application will check the status of the folder every 5 seconds.\n\n" \
        "Press ENTER at the filename field to refresh instantly\n\n" \
        "Show this message at startup?"

    def __init__(self):
        super().__init__()
        self.title(self.TITLE)
        icon = tk.PhotoImage(file=os.path.join(config.get_base_dir(), "gfx", "isdep.png"))
        self.iconphoto(False, icon)
        self.geometry(self.WINDOW_SIZE)
        self.resizable(False, False)
        self.poll_interval = self.POLL_INTERVAL

        self.style = ttk.Style()
        self.style.configure("TButton", padding=self.DEFAULT_PADDING, font=(self.DEFAULT_FONT, self.DEFAULT_FONT_SIZE))
        self.style.configure("TEntry", padding=self.DEFAULT_PADDING, font=(self.DEFAULT_FONT, self.DEFAULT_FONT_SIZE))

        self.create_widgets()
        self.poll()

    def run_checks(self):
        if sound.is_muted():
            self.set_title("[MUTED] " + self.TITLE)
        else:
            self.set_title(self.TITLE)

    def toggle_mute(self):
        sound.mute()
        self.run_checks()

    def set_title(self, title):
        self.title(title)

    def create_widgets(self):
        self.path_frame = ttk.Frame(self)
        self.path_frame.pack(fill=tk.X, padx=10)

        self.filename_frame = ttk.Frame(self)
        self.filename_frame.pack(fill=tk.X, padx=10)

        self.path_entry = ttk.Entry(self.path_frame, style="TEntry")
        self.path_entry.pack(fill=tk.X, expand=True, side=tk.LEFT)
        self.path_entry.insert(0, config.path if config.exists() else self.DEFAULT_ENTRY_TEXT)
        self.path_entry.bind("<KeyRelease>", lambda event: self.after(100, self.update_status))
        self.path_entry.bind("<FocusIn>", lambda event: self.clear_text(self.path_entry))
        self.path_entry.bind("<FocusOut>", lambda event: self.reinsert_text(self.path_entry))

        self.path_button = ttk.Button(self.path_frame, text="Browse", command=self.browse, style="TButton")
        self.path_button.pack(side=tk.RIGHT)

        self.filename = ttk.Entry(self.filename_frame, style="TEntry")
        self.filename.pack(fill=tk.X, expand=True, side=tk.LEFT)
        self.filename.insert(0, config.filename if config.exists() else self.DEFAULT_FILENAME_TEXT)
        self.filename.bind("<KeyRelease>", lambda event: self.after(100, self.update_status))
        self.filename.bind("<Return>", lambda event: self.update_status())
        self.filename.bind("<FocusIn>", lambda event: self.clear_text(self.filename))
        self.filename.bind("<FocusOut>", lambda event: self.reinsert_text(self.filename))

        self.mute_button = ttk.Button(self.filename_frame, text="Mute", command=lambda: self.toggle_mute(), style="TButton")
        self.mute_button.pack(side=tk.RIGHT)

        self.canvas = tk.Canvas(self, width=400, height=50)
        self.canvas.pack(padx=10, pady=(10, 10))

        self.status_label = self.canvas.create_text(200, 25, font=(self.DEFAULT_FONT, self.DEFAULT_FONT_SIZE, "bold"))
        self.canvas.bind("<Button-1>", lambda event: self.show_info_control(True))

    def clear_text(self, field):
        current_text = field.get()
        if current_text == self.DEFAULT_ENTRY_TEXT or current_text == self.DEFAULT_FILENAME_TEXT:
            field.delete(0, tk.END)

    def reinsert_text(self, field):
        current_text = field.get()
        if current_text == "":
            field.insert(0, self.DEFAULT_ENTRY_TEXT if field == self.path_entry else self.DEFAULT_FILENAME_TEXT)

    def browse(self):
        path = filedialog.askdirectory()
        if path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, path)
            self.update_status()

    def update_status(self):
        path = self.path_entry.get()
        filename = self.filename.get()
        config.path = path
        config.filename = filename
        config.save()
        status_checker = StatusChecker(path, filename)
        status, bg_color, time = status_checker.check_status()
        self.canvas.configure(background=bg_color)
        self.canvas.itemconfigure(
            self.status_label, text=f"{status} since {time}" if time else status, fill="white" if bg_color == "red" else "black")

    def poll(self):
        self.update_status()
        self.after(self.poll_interval, self.poll)

    def show_info_control(self, wasClick=False):
        if config.show_info:
            show_info = self.show_info_message()
            config.show_info = True if show_info else False

        elif (wasClick or config.show_info is None):
            show_info = self.show_info_message()
            config.show_info = True if show_info else False

        config.save()

    def show_info_message(self):
        result = tk.messagebox.askyesno(
            self.INFO_TITLE, self.INFO_TEXT, icon="info", default="yes")
        self.focus_force()
        return result

class Sound:
    def __init__(self) -> None:
        mixer.init()

        self.ok_sound_path = os.path.join(config.base_dir, "sfx", "ok.mp3")
        self.error_sound_path = os.path.join(config.base_dir, "sfx", "error.mp3")
        self.ok_sound = mixer.Sound(self.ok_sound_path)
        self.error_sound = mixer.Sound(self.error_sound_path)
        self.muted = False

    def play_error(self):
        if not self.muted:
            self.error_sound.play()

    def play_success(self):
        if not self.muted:
            self.ok_sound.play()

    def mute(self):
        self.muted = True if not self.muted else False

    def is_muted(self):
        return self.muted


class History:
    def __init__(self) -> None:
        self.status_history = []

    def add_status(self, status):
        status_history_size = len(self.status_history)

        if status_history_size >= 10:
            self.status_history.pop(0)

        if status_history_size == 0:
            self.status_history.append(status)
        elif status is not self.status_history[-1]:
            if status is StatusChecker.STATUS_DEPLOYED:
                sound.play_success()
            else:
                sound.play_error()

            self.status_history.append(status)

class Config:
    def __init__(self, path=None, filename=None, show_info=None) -> None:
        self.base_dir = getattr(sys, '_ISDEP', os.path.abspath(os.path.dirname(__file__)))
        self.path = path
        self.filename = filename
        self.show_info = show_info

    def save(self):
        with open("config.json", "w") as f:
            json.dump(self.__dict__, f)

    def load(self):
        if os.path.exists("config.json"):
            with open("config.json", "r") as f:
                config = json.load(f)
                self.path = config["path"]
                self.filename = config["filename"]
                self.show_info = config["show_info"]

    def exists(self):
        return os.path.exists("config.json")

    def get_base_dir(self):
        return self.base_dir


if __name__ == "__main__":
    config = Config()
    config.load()
    history = History()
    sound = Sound()
    app = IsDeployedApp()
    app.show_info_control()
    app.update_status()
    app.mainloop()
