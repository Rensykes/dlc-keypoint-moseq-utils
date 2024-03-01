import matplotlib.pyplot as plt
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
