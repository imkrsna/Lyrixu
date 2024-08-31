from PIL import Image
from os import path, makedirs
from moviepy.editor import VideoFileClip
from .youtube import YouTube

class Editor():
    def __init__(self, url: str, project_path: str):
        self.video = YouTube(url, project_path)
        self.project_path = project_path
    
    def download_video(self):
        self.video.download()

    def extract_frames(self, fps: float = 0.5):
        output_path = path.join(self.project_path, f"tmp/extract/{self.video.id}/")
        makedirs(output_path)
        clip = VideoFileClip(self.video.export_uri + ".mp4")

        for i, frame in enumerate(clip.iter_frames(fps=fps)):
            frame_path = path.join(output_path, f"frame_{i:08d}.jpg")
            image = Image.fromarray(frame)
            image.save(frame_path)
        
        clip.close()