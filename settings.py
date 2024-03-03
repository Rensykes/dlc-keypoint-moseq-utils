# settings.py

import tkinter as tk
from tkinter import messagebox

class SettingsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Settings")

        # Default converted video prefix
        self.label = tk.Label(self, text="Default converted video prefix:")
        self.label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.text_area = tk.Text(self, height=1, width=30)
        self.text_area.grid(row=0, column=1, padx=10, pady=5, sticky="we")
        
        button = tk.Button(self, image=self.parent.icons["help_icon"], command=self.show_message)
        button.grid(row=0, column=2, padx=10, pady=5)
        
        # Checkbox for renaming video upon conversion
        self.rename_var = tk.BooleanVar()
        self.rename_checkbox = tk.Checkbutton(self, text="Rename video upon conversion", variable=self.rename_var,
                                              command=self.toggle_prefix_entry)
        self.rename_checkbox.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        # Prefix to add to the original video upon conversion
        self.prefix_label = tk.Label(self, text="Prefix to add to the original video upon conversion:")
        self.prefix_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.prefix_text_area = tk.Text(self, height=1, width=30, state=tk.DISABLED)
        self.prefix_text_area.grid(row=2, column=1, padx=10, pady=5, sticky="we")

        
        self.apply_button = tk.Button(self, text="Apply", command=self.apply_settings)
        self.apply_button.grid(row=3, column=1, padx=5, pady=10, sticky="e")

        self.cancel_button = tk.Button(self, text="Cancel", command=self.cancel_settings)
        self.cancel_button.grid(row=3, column=2, padx=5, pady=10, sticky="e")
        
        # Load settings from parent
        self.load_settings()

    def load_settings(self):
        # Load settings from self.parent.settings or settings.ini
        self.text_area.insert(tk.END, self.parent.settings.get("converted_video_prefix", ""))
        self.rename_var.set(self.parent.settings.get("rename_original_video", False))
        self.toggle_prefix_entry()

        self.prefix_text_area.insert(tk.END, self.parent.settings.get("original_video_prefix", ""))

    def apply_settings(self):
        # converted_video_prefix
        new_video_prefix = self.text_area.get("1.0", "end-1c")
        if not new_video_prefix.endswith('_'):
            new_video_prefix += '_'
        self.parent.settings["converted_video_prefix"] = new_video_prefix
        
        # rename_original_video
        rename_original_video = self.rename_var.get()
        self.parent.settings["rename_original_video"] = rename_original_video

        # original_video_prefix
        original_video_prefix = None
        if self.rename_var.get():
            original_video_prefix = self.prefix_text_area.get("1.0", "end-1c")
            if not new_video_prefix.endswith('_'):
                original_video_prefix += '_'
        else:
            original_video_prefix = ""  # Empty string if checkbox is not checked
        self.parent.settings["original_video_prefix"] = original_video_prefix
        
        self.parent.save_settings(converted_video_prefix=new_video_prefix, rename_original_video=rename_original_video, original_video_prefix=original_video_prefix)
        self.destroy()

    def cancel_settings(self):
        self.destroy()

    def show_message(self):
        messagebox.showinfo("Default converted video prefix", "When the input field Output Name is not filled, the video will be saved using the following format: <prefix>_<old_video_name>")
            
    def toggle_prefix_entry(self):
        # Enable prefix text area if checkbox is checked, otherwise disable it
        state = tk.NORMAL if self.rename_var.get() else tk.DISABLED
        self.prefix_text_area.config(state=state)