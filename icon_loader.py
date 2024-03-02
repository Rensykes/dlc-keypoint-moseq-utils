# icon_loader.py

import os
from PIL import Image, ImageTk

def load_icons():
    icons_folder = os.path.join("assets", "icons")
    icon_paths = {
        "main_icon": os.path.join(icons_folder, "mouse_1.ico"),
        "help_icon": os.path.join(icons_folder, "question_mark_2.png"),
    }
    icons = {}
    for name, path in icon_paths.items():
        icon = Image.open(path).resize((20, 20), Image.ANTIALIAS)
        icons[name] = ImageTk.PhotoImage(icon)
    return icons
