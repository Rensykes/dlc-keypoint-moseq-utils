import tkinter as tk
import os
from tkinter import filedialog, messagebox
from moviepy.editor import VideoFileClip
from crop_selector import CropSelector
from PIL import Image, ImageTk

class VideoConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Video Converter")
        self.load_icons()

        self.padding_x = 10
        self.padding_y = 2
        self.width = 50

        self.create_widgets()

        self.crop_area = None

    def load_icons(self):
        icons_folder = os.path.join("assets", "icons")
        icon_path = os.path.join(icons_folder, "question-mark.png")
        icon = Image.open(icon_path).resize((20, 20), Image.ANTIALIAS)
        self.help_icon = ImageTk.PhotoImage(icon)

    def create_widgets(self):
        self.create_input_widgets()
        self.create_output_widgets()
        self.create_name_widgets()
        self.create_format_widgets()
        self.create_info_widgets()
        self.create_crop_widgets()
        self.create_conversion_widgets()

    def create_input_widgets(self):
        self.input_path_label = tk.Label(self, text="Input Video Path:")
        self.input_path_label.grid(row=0, column=0, padx=self.padding_x, pady=self.padding_y)

        self.input_path_entry = tk.Entry(self, width=self.width)
        self.input_path_entry.grid(row=0, column=1, padx=self.padding_x, pady=self.padding_y)

        self.input_path_button = tk.Button(self, text="Browse", command=self.browse_input_path)
        self.input_path_button.grid(row=0, column=2, padx=self.padding_x, pady=self.padding_y)
        
        self.input_path_help_button = tk.Button(self, image=self.help_icon, command=self.show_input_path_help)
        self.input_path_help_button.grid(row=0, column=3, padx=self.padding_x, pady=self.padding_y)

    def create_output_widgets(self):
        self.output_path_label = tk.Label(self, text="Output Video Folder:")
        self.output_path_label.grid(row=1, column=0, padx=self.padding_x, pady=self.padding_y)

        self.output_path_entry = tk.Entry(self, width=self.width)
        self.output_path_entry.grid(row=1, column=1, padx=self.padding_x, pady=self.padding_y)

        self.output_path_button = tk.Button(self, text="Browse", command=self.browse_output_path)
        self.output_path_button.grid(row=1, column=2, padx=self.padding_x, pady=self.padding_y)

        self.output_path_help_button = tk.Button(self, image=self.help_icon, command=self.show_output_path_help)
        self.output_path_help_button.grid(row=1, column=3, padx=self.padding_x, pady=self.padding_y)

    def create_name_widgets(self):
        self.name_label = tk.Label(self, text="Output Name:")
        self.name_label.grid(row=2, column=0, padx=self.padding_x, pady=self.padding_y)

        self.name_entry = tk.Entry(self, width=self.width)
        self.name_entry.grid(row=2, column=1, padx=self.padding_x, pady=self.padding_y)

        self.name_help_button = tk.Button(self, image=self.help_icon, command=self.show_name_help)
        self.name_help_button.grid(row=2, column=2, padx=self.padding_x, pady=self.padding_y)

    def create_format_widgets(self):
        self.format_label = tk.Label(self, text="Output Format:")
        self.format_label.grid(row=3, column=0, padx=self.padding_x, pady=self.padding_y)

        self.format_var = tk.StringVar(self)
        self.format_var.set("mp4")  # default format
        self.format_dropdown = tk.OptionMenu(self, self.format_var, "mp4", "mov", "avi", command=self.format_dropdown_callback)
        self.format_dropdown.config(width=self.width)  # Set the width of the OptionMenu
        self.format_dropdown.grid(row=3, column=1, padx=self.padding_x, pady=self.padding_y)

        self.format_help_button = tk.Button(self, image=self.help_icon, command=self.show_format_help)
        self.format_help_button.grid(row=3, column=2, padx=self.padding_x, pady=self.padding_y)

    def create_info_widgets(self):
        self.fps_label = tk.Label(self, text="FPS:")
        self.fps_label.grid(row=4, column=0, padx=self.padding_x, pady=self.padding_y)
        self.fps_value_label = tk.Label(self, text="")
        self.fps_value_label.grid(row=4, column=1, padx=self.padding_x, pady=self.padding_y)

        self.size_label = tk.Label(self, text="Size:")
        self.size_label.grid(row=5, column=0, padx=self.padding_x, pady=self.padding_y)
        self.size_value_label = tk.Label(self, text="")
        self.size_value_label.grid(row=5, column=1, padx=self.padding_x, pady=self.padding_y)

    def create_crop_widgets(self):
        self.crop_button = tk.Button(self, text="Select Crop Area", command=self.select_crop_area)
        self.crop_button.grid(row=6, column=0, columnspan=4, padx=self.padding_x, pady=self.padding_y)

    def create_conversion_widgets(self):
        self.convert_button = tk.Button(self, text="Convert", command=self.convert_video)
        self.convert_button.grid(row=7, column=0, columnspan=4, padx=self.padding_x, pady=self.padding_y)

    def browse_input_path(self):
        input_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.avi *.mkv *.mov")])
        if input_path:
            self.input_path_entry.delete(0, tk.END)
            self.input_path_entry.insert(0, input_path)

    def browse_output_path(self):
        output_path = filedialog.askdirectory()
        if output_path:
            self.output_path_entry.delete(0, tk.END)
            self.output_path_entry.insert(0, output_path)

    def show_input_path_help(self):
        messagebox.showinfo("Input Path", "Select the path of the input video.")

    def show_output_path_help(self):
        messagebox.showinfo("Output Path", "Select the folder where the converted video will be saved.")

    def show_name_help(self):
        messagebox.showinfo("Output Name", "Specify the name of the output video file (optional).")

    def show_format_help(self):
        messagebox.showinfo("Output Format", "Select the desired output format for the converted video.")

    def select_crop_area(self):
        input_path = self.input_path_entry.get()
        if not input_path:
            messagebox.showerror("Error", "Please select input video path first.")
            return

        selector = CropSelector(input_path)
        self.crop_area = selector.select_crop_area()
        self.update_video_info(input_path)

    def convert_video(self):
        input_path = self.input_path_entry.get()
        output_path = self.output_path_entry.get() or None  # use None if not set
        output_format = self.format_var.get()
        output_name = self.name_entry.get() or None  # use None if not set

        if not input_path:
            messagebox.showerror("Error", "Please select input video path.")
            return

        if not self.crop_area:
            messagebox.showerror("Error", "Please select crop area.")
            return

        video = VideoFileClip(input_path)

        x1, y1, x2, y2 = self.crop_area
        x1, y1, x2, y2 = self.check_even_dimensions(x1, y1, x2, y2)

        video = video.crop(x1, y1, x2, y2)

        if output_name is None:
            output_name = input_path.split('/')[-1].split('.')[0]  # get name from input path

        if output_path is None:
            output_path = '/'.join(input_path.split('/')[:-1])  # get folder from input path

        output_file = f"{output_path}/{output_name}.{output_format}"

        video.write_videofile(output_file, codec='libx264', fps=video.fps, audio_codec='aac', preset='ultrafast')
        messagebox.showinfo("Success", "Video conversion complete.")

    def check_even_dimensions(self, x1, y1, x2, y2):
        width = x2 - x1
        height = y2 - y1

        print("Selected width: " + str(width) + " Selected height: " + str(height))
        # Ensure width and height are even
        if width % 2 != 0:
            x2 -= 1
            print("Width not even, reducing it by 1")
        if height % 2 != 0:
            y2 -= 1
            print("Height not even, reducing it by 1")

        return x1, y1, x2, y2

    def format_dropdown_callback(self, value):
        # Disable options other than "mp4"
        if value != "mp4":
            self.format_dropdown["menu"].entryconfigure("mov", state="disabled")
            self.format_dropdown["menu"].entryconfigure("avi", state="disabled")
        else:
            self.format_dropdown["menu"].entryconfigure("mov", state="normal")
            self.format_dropdown["menu"].entryconfigure("avi", state="normal")

    def update_video_info(self, input_path):
        video = VideoFileClip(input_path)
        self.fps_value_label.config(text=f"{video.fps:.2f}")
        self.size_value_label.config(text=f"{video.size[0]} x {video.size[1]}")

if __name__ == "__main__":
    app = VideoConverterApp()
    app.mainloop()
