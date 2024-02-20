import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.editor import VideoFileClip
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Rectangle

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
    # def browse_input_path(self):
    #     input_path = filedialog.askopenfilename()
    #     if input_path:
    #         self.input_path_entry.delete(0, tk.END)
    #         self.input_path_entry.insert(0, input_path)

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
        video = video.crop(x1, y1, x2, y2)

        video.write_videofile(output_file, codec='mpeg4', fps=video.fps, audio=False, preset='ultrafast')
        messagebox.showinfo("Success", "Video conversion complete.")

class CropSelector:
    def __init__(self, video_path):
        self.video = VideoFileClip(video_path)
        self.frame = self.video.get_frame(0)
        self.crop_area = None

    def select_crop_area(self):
        fig, ax = plt.subplots()
        ax.imshow(self.frame)
        plt.title('Select crop area by clicking and dragging')

        def on_click(event):
            self.x1, self.y1 = event.xdata, event.ydata

        def on_release(event):
            self.x2, self.y2 = event.xdata, event.ydata
            self.crop_area = (int(self.x1), int(self.y1), int(self.x2), int(self.y2))
            ax.add_patch(Rectangle((self.x1, self.y1), self.x2 - self.x1, self.y2 - self.y1, linewidth=1, edgecolor='r', facecolor='none'))
            fig.canvas.draw()

        fig.canvas.mpl_connect('button_press_event', on_click)
        fig.canvas.mpl_connect('button_release_event', on_release)

        plt.show()

        return self.crop_area

if __name__ == "__main__":
    app = VideoConverterApp()
    app.mainloop()
