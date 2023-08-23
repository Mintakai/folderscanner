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
import os
import glob


class StatusChecker:
    STATUS_DOWN = "[DOWN]"
    STATUS_DEPLOYED = "[DEPLOYED]"
    STATUS_DEPLOYING = "[DEPLOYING]"

    COLOR_PINK = "pink"
    COLOR_LIGHT_GREEN = "light green"
    COLOR_YELLOW = "yellow"

    def __init__(self, path):
        self.path = path

    def check_status(self):
        status = self.STATUS_DOWN
        bg_color = self.COLOR_PINK
        time = ""

        if os.path.exists(self.path) and os.path.isdir(self.path):
            deployed_files = glob.glob(os.path.join(self.path, "*.deployed"))
            deploying_files = glob.glob(os.path.join(self.path, "*.isdeploying"))

            if deployed_files:
                status = self.STATUS_DEPLOYED
                bg_color = self.COLOR_LIGHT_GREEN
                time = self.get_latest_file_time(deployed_files)
            elif deploying_files:
                status = self.STATUS_DEPLOYING
                bg_color = self.COLOR_YELLOW
                time = self.get_latest_file_time(deploying_files)
            else:
                time = datetime.fromtimestamp(os.path.getctime(self.path)).strftime('%Y-%m-%d %H:%M')

        return status, bg_color, time

    def get_latest_file_time(self, files):
        latest_file = max(files, key=os.path.getctime)
        return datetime.fromtimestamp(os.path.getctime(latest_file)).strftime('%Y-%m-%d %H:%M')


class IsDeployedApp(tk.Tk):
    TITLE = "Is LIMS up?"
    WINDOW_SIZE = "400x120"
    DEFAULT_FONT = "Helvetica"
    DEFAULT_FONT_SIZE = 10

    POLL_INTERVAL = 5000
    DEFAULT_ENTRY_TEXT = "Path to jboss deployments folder"

    def __init__(self):
        super().__init__()
        self.title(self.TITLE)
        self.geometry(self.WINDOW_SIZE)
        self.resizable(False, False)
        self.poll_interval = self.POLL_INTERVAL

        self.style = ttk.Style()
        self.style.configure("TButton", padding=5, font=(self.DEFAULT_FONT, self.DEFAULT_FONT_SIZE))
        self.style.configure("TLabel", font=(self.DEFAULT_FONT, self.DEFAULT_FONT_SIZE))
        self.style.configure("TEntry", padding=5, font=(self.DEFAULT_FONT, self.DEFAULT_FONT_SIZE))

        self.create_widgets()
        self.poll()

    def create_widgets(self):
        self.path_frame = ttk.Frame(self)
        self.path_frame.pack(fill=tk.X, padx=10, pady=(10, 0))

        self.path_entry = ttk.Entry(self.path_frame, foreground="grey")
        self.path_entry.pack(fill=tk.X, expand=True, side=tk.LEFT)
        self.path_entry.insert(0, self.DEFAULT_ENTRY_TEXT)
        self.path_entry.bind("<FocusIn>", self.on_entry_focus_in)
        self.path_entry.bind("<FocusOut>", self.on_entry_focus_out)

        self.path_button = ttk.Button(
            self.path_frame, text="Browse", command=self.browse)
        self.path_button.pack(side=tk.RIGHT)

        self.canvas = tk.Canvas(self, width=400, height=50)
        self.canvas.pack(padx=10, pady=(10, 10))

        self.status_label = self.canvas.create_text(
            200, 25, font=(self.DEFAULT_FONT, self.DEFAULT_FONT_SIZE, "bold"))

    def on_entry_focus_in(self, event):
        if self.path_entry.get() == self.DEFAULT_ENTRY_TEXT:
            self.path_entry.delete(0, tk.END)
            self.path_entry.configure(foreground="black")

    def on_entry_focus_out(self, event):
        if not self.path_entry.get():
            self.path_entry.insert(0, self.DEFAULT_ENTRY_TEXT)
            self.path_entry.configure(foreground="grey")

    def browse(self):
        path = filedialog.askdirectory()
        if path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, path)
            self.update_status()

    def update_status(self):
        path = self.path_entry.get()
        status_checker = StatusChecker(path)
        status, bg_color, time = status_checker.check_status()

        self.canvas.configure(background=bg_color)
        self.canvas.itemconfigure(self.status_label, text= f"{status} since {time}" if time else status)

    def poll(self):
        self.update_status()
        self.after(self.poll_interval, self.poll)


if __name__ == "__main__":
    app = IsDeployedApp()
    app.mainloop()
