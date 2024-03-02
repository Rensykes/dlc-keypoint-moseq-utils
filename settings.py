# settings.py

import tkinter as tk
from tkinter import messagebox

class SettingsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Settings")

        self.label = tk.Label(self, text="Default converted video prefix:")
        self.label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.text_area = tk.Text(self, height=1, width=30)
        self.text_area.grid(row=0, column=1, padx=10, pady=5, sticky="we")
        
        button = tk.Button(self, image=self.parent.icons["help_icon"], command=self.show_message)
        button.grid(row=0, column=2, padx=10, pady=5)
        
        self.apply_button = tk.Button(self, text="Apply", command=self.apply_settings)
        self.apply_button.grid(row=1, column=1, padx=5, pady=10, sticky="e")

        self.cancel_button = tk.Button(self, text="Cancel", command=self.cancel_settings)
        self.cancel_button.grid(row=1, column=2, padx=5, pady=10, sticky="e")

    def apply_settings(self):
        new_video_prefix = self.text_area.get("1.0", "end-1c")
        if not new_video_prefix.endswith('_'):
            new_video_prefix += '_'
        self.parent.settings["converted_video_prefix"] = new_video_prefix
        self.parent.save_settings(converted_video_prefix=new_video_prefix)
        self.destroy()

    def cancel_settings(self):
        self.destroy()

    def show_message(self):
        messagebox.showinfo("Default converted video prefix", "When the input field Output Name is not filled, the video will be saved using the following format: <prefix>_<old_video_name>")