import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.editor import VideoFileClip
from crop_selector import CropSelector

class VideoConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Video Converter")

        self.input_path_label = tk.Label(self, text="Input Video Path:")
        self.input_path_label.grid(row=0, column=0)

        self.input_path_entry = tk.Entry(self, width=50)
        self.input_path_entry.grid(row=0, column=1)

        self.input_path_button = tk.Button(self, text="Browse", command=self.browse_input_path)
        self.input_path_button.grid(row=0, column=2)

        self.output_path_label = tk.Label(self, text="Output Video Folder:")
        self.output_path_label.grid(row=1, column=0)

        self.output_path_entry = tk.Entry(self, width=50)
        self.output_path_entry.grid(row=1, column=1)

        self.output_path_button = tk.Button(self, text="Browse", command=self.browse_output_path)
        self.output_path_button.grid(row=1, column=2)

        self.name_label = tk.Label(self, text="Output Name:")
        self.name_label.grid(row=2, column=0)

        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=2, column=1)

        self.format_label = tk.Label(self, text="Output Format:")
        self.format_label.grid(row=3, column=0)

        self.format_entry = tk.Entry(self)
        self.format_entry.grid(row=3, column=1)

        self.crop_button = tk.Button(self, text="Select Crop Area", command=self.select_crop_area)
        self.crop_button.grid(row=4, column=0, columnspan=3)

        self.convert_button = tk.Button(self, text="Convert", command=self.convert_video)
        self.convert_button.grid(row=5, column=0, columnspan=3)

        self.crop_area = None

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

    def select_crop_area(self):
        input_path = self.input_path_entry.get()
        if not input_path:
            messagebox.showerror("Error", "Please select input video path first.")
            return

        selector = CropSelector(input_path)
        self.crop_area = selector.select_crop_area()

    def convert_video(self):
        input_path = self.input_path_entry.get()
        output_path = self.output_path_entry.get()
        output_format = self.format_entry.get()
        output_name = self.name_entry.get()

        if not (input_path and output_path and output_format and output_name):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        if not self.crop_area:
            messagebox.showerror("Error", "Please select crop area first.")
            return

        output_file = f"{output_path}/{output_name}.{output_format}"
        video = VideoFileClip(input_path)

        x1, y1, x2, y2 = self.crop_area

        x1, y1, x2, y2 = self.check_even_dimensions(x1, y1, x2, y2)

        video = video.crop(x1, y1, x2, y2)

        video.write_videofile(output_file, codec='libx264', fps=video.fps, audio_codec='aac', preset='ultrafast')
        messagebox.showinfo("Success", "Video conversion complete.")

    '''
    Utility method used to check if the width and height of the cropped video are even.
    https://zulko.github.io/moviepy/FAQ.html#moviepy-generated-a-video-that-cannot-be-read-by-my-favorite-player
    One of the video s dimensions were not even, for instance 720x405, and you used a MPEG4 codec like libx264 (default in MoviePy). 
    In this case the video generated uses a format that is readable only on some readers like VLC.
    '''
    def check_even_dimensions(x1, y1, x2, y2):
        width = x2 - x1
        height = y2 - y1

        print("Selected width: " + str(width) + " Selected height: " + str(height))
        # Ensure width and height are even
        if width % 2 != 0:
            x2 -= 1
            print("Width not even, reducing it by 1")
        if height % 2 != 0:
            y2 -= 1
            print("Width not even, reducing it by 1")

        return x1, y1, x2, y2