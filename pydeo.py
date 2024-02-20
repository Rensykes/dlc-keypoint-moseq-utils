import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Rectangle
from moviepy.editor import VideoFileClip

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

from PIL import Image

def convert_video(input_path, output_path, target_format='mp4', crop=None, resize=None):
    video = VideoFileClip(input_path)

    if crop:
        x1, y1, x2, y2 = crop
        video = video.crop(x1, y1, x2, y2)

    if resize:
        width, height = resize
        # Specify resampling method here (e.g., Image.BILINEAR, Image.BICUBIC)
        video = video.resize((width, height))

    video.write_videofile(output_path)

# Example usage:
input_path = 'video1.mp4'
output_path = 'output_video.mp4'

selector = CropSelector(input_path)
crop_area = selector.select_crop_area()

# Define resize dimensions (width, height) - optional
resize_dimensions = (640, 480)

convert_video(input_path, output_path, crop=crop_area, resize=resize_dimensions)
