import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.editor import VideoFileClip
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Rectangle
from tkinter.ttk import Notebook  # Importing ttk separately

class VideoConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Video Converter")

        self.tabControl = Notebook(self)
        self.tabControl.pack(expand=1, fill="both")

        self.convert_frames_tab = tk.Frame(self.tabControl)
        self.tabControl.add(self.convert_frames_tab, text="Convert Individual Videos")
        self.setup_convert_frames_tab()

        self.convert_multiple_tab = tk.Frame(self.tabControl)
        self.tabControl.add(self.convert_multiple_tab, text="Convert Multiple Videos")
        self.setup_convert_multiple_tab()

    def setup_convert_frames_tab(self):
        self.input_path_label = tk.Label(self.convert_frames_tab, text="Input Video Path:")
        self.input_path_label.grid(row=0, column=0)

        self.input_path_entry = tk.Entry(self.convert_frames_tab, width=50)
        self.input_path_entry.grid(row=0, column=1)

        self.input_path_button = tk.Button(self.convert_frames_tab, text="Browse", command=self.browse_input_path)
        self.input_path_button.grid(row=0, column=2)

        self.output_path_label = tk.Label(self.convert_frames_tab, text="Output Video Folder:")
        self.output_path_label.grid(row=1, column=0)

        self.output_path_entry = tk.Entry(self.convert_frames_tab, width=50)
        self.output_path_entry.grid(row=1, column=1)

        self.output_path_button = tk.Button(self.convert_frames_tab, text="Browse", command=self.browse_output_path)
        self.output_path_button.grid(row=1, column=2)

        self.format_label = tk.Label(self.convert_frames_tab, text="Output Format:")
        self.format_label.grid(row=2, column=0)

        self.format_entry = tk.Entry(self.convert_frames_tab)
        self.format_entry.grid(row=2, column=1)

        self.crop_button = tk.Button(self.convert_frames_tab, text="Select Crop Area", command=self.select_crop_area)
        self.crop_button.grid(row=3, column=0, columnspan=3)

        self.convert_button = tk.Button(self.convert_frames_tab, text="Convert", command=self.convert_video)
        self.convert_button.grid(row=4, column=0, columnspan=3)

        self.crop_area = None

    def setup_convert_multiple_tab(self):
        self.input_path_label_multiple = tk.Label(self.convert_multiple_tab, text="Input Video Folder:")
        self.input_path_label_multiple.grid(row=0, column=0)

        self.input_path_entry_multiple = tk.Entry(self.convert_multiple_tab, width=50)
        self.input_path_entry_multiple.grid(row=0, column=1)

        self.input_path_button_multiple = tk.Button(self.convert_multiple_tab, text="Browse", command=self.browse_input_path_multiple)
        self.input_path_button_multiple.grid(row=0, column=2)

        self.output_format_label = tk.Label(self.convert_multiple_tab, text="Output Format:")
        self.output_format_label.grid(row=1, column=0)

        self.output_format_entry = tk.Entry(self.convert_multiple_tab)
        self.output_format_entry.grid(row=1, column=1)

        self.convert_button_multiple = tk.Button(self.convert_multiple_tab, text="Convert Multiple Videos", command=self.convert_multiple_videos)
        self.convert_button_multiple.grid(row=2, column=0, columnspan=3)

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

    def browse_input_path_multiple(self):
        input_path = filedialog.askdirectory()
        if input_path:
            self.input_path_entry_multiple.delete(0, tk.END)
            self.input_path_entry_multiple.insert(0, input_path)

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

        if not (input_path and output_path and output_format):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        if not self.crop_area:
            messagebox.showerror("Error", "Please select crop area first.")
            return

        output_file = os.path.join(output_path, os.path.splitext(os.path.basename(input_path))[0] + '.' + output_format)
        video = VideoFileClip(input_path)

        x1, y1, x2, y2 = self.crop_area
        video = video.crop(x1, y1, x2, y2)

        video.write_videofile(output_file, codec='libx264', fps=video.fps, audio_codec='aac', preset='ultrafast')
        messagebox.showinfo("Success", "Video conversion complete.")

    def convert_multiple_videos(self):
        input_folder = self.input_path_entry_multiple.get()
        output_format = self.output_format_entry.get()

        if not (input_folder and output_format):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        for root, dirs, files in os.walk(input_folder):
            for file in files:
                if file.lower().endswith('.mp4') or file.lower().endswith('.avi') or file.lower().endswith('.mkv') or file.lower().endswith('.mov'):
                    input_path = os.path.join(root, file)
                    output_path = os.path.join(root, os.path.splitext(file)[0] + '.' + output_format)
                    video = VideoFileClip(input_path)

                    x1, y1, x2, y2 = self.get_crop_area(input_path)
                    video = video.crop(x1, y1, x2, y2)

                    video.write_videofile(output_path, codec='libx264', fps=video.fps, audio_codec='aac', preset='ultrafast')

        messagebox.showinfo("Success", "All videos converted.")

    def get_crop_area(self, video_path):
        selector = CropSelector(video_path)
        return selector.select_crop_area()

class CropSelector:
    def __init__(self, video_path):
        self.video = VideoFileClip(video_path)
        self.frame = self.video.get_frame(0)
        self.crop_area = None

    def select_crop_area(self):
        fig, ax = plt.subplots()
        ax.imshow(self.frame)
        plt.title("Select Crop Area")
        plt.xlabel("Press Enter to Confirm Selection")

        def on_click(event):
            if event.button == 1:
                x1, y1 = event.xdata, event.ydata
                self.crop_area = [x1, y1, x1, y1]

        def on_release(event):
            if event.button == 1:
                x2, y2 = event.xdata, event.ydata
                self.crop_area[2:] = [x2, y2]
                plt.close()

        cid1 = fig.canvas.mpl_connect('button_press_event', on_click)
        cid2 = fig.canvas.mpl_connect('button_release_event', on_release)

        plt.show()

        return self.crop_area

if __name__ == "__main__":
    app = VideoConverterApp()
    app.mainloop()
