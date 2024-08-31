import random
import string
from os import path, makedirs
from pytubefix import YouTube as YT
from pytubefix.cli import on_progress


class YouTube():
    def __init__(self, url: str, project_path: str):
        self.url = url
        self.id = "".join([random.choice(string.ascii_letters) for _ in range(10)])
        self.video = YT(url=self.url, on_progress_callback=on_progress)
        self.project_path = project_path
        self.export_uri = None

    def download(self):
        # psudo output path
        output_path = path.join(self.project_path, f"tmp/downloads/{self.id}/")
        self.export_uri = output_path + self.id
        
        # creating path
        makedirs(output_path)
        
        # downloding video
        stream = self.video.streams.get_highest_resolution()
        stream.download(output_path=output_path, filename=self.id + ".mp4") # video
        
        # downloding audio
        stream = self.video.streams.get_audio_only()
        stream.download(output_path=output_path, filename=self.id, mp3=True) # audio