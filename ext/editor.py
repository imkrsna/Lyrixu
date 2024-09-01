from os import path, listdir

from .helper import Project
from .ocr import OCR

from pytubefix import YouTube
from pytubefix.cli import on_progress

from moviepy.editor import VideoFileClip
from PIL import Image

from tqdm import tqdm


class LRC():
    def __init__(self, url: str, PROJECT: Project):
        self.url = url
        self.PROJECT = PROJECT
        self.OCR = OCR()
        self.video = YouTube(url=self.url, on_progress_callback=on_progress)
    
    def download_video(self):
        # downloading video
        stream = self.video.streams.get_highest_resolution()
        stream.download(output_path=self.PROJECT.downloads_path, filename=self.PROJECT.input_video)
        
    def download_audio(self):
        # downloading audio
        stream = self.video.streams.get_audio_only()
        stream.download(output_path=self.PROJECT.downloads_path, filename=self.PROJECT.input_audio)

    def extract_frames(self):
        # opening input clip
        clip = VideoFileClip(self.PROJECT.input_video_path)
        
        # loop thought all frames
        images = []
        for i, frame in enumerate(clip.iter_frames(fps=self.PROJECT.extract_fps)):
            image = Image.fromarray(frame)

            # crop height offset
            crop = self.PROJECT.extract_crop
            width, height = image.width, image.height
            image = image.crop((crop, crop, width - crop, height - crop))

            # saving image
            # image.save(self.PROJECT.extract_frames.format(i))
            images.append(image)

        # export pdf
        images[0].save(self.PROJECT.extract_frames_pdf, save_all=True, append_images=images[1:])
 
        # closing input clip
        clip.close()

    def generate_lrc(self):
        lyrics = self.get_lyrics()
        # self.write_lrc(lyrics)
        return self.read_lrc()

    def get_lyrics(self):
        stamp = self.OCR.extract_text(self.PROJECT.extract_frames_pdf)
        lyrics = []
        lyrics.append(stamp[0])
        for text in stamp[1:]:
            if (text[1] != lyrics[-1][1]):
                lyrics.append(text)
        
        return lyrics

    def write_lrc(self, lyrics: list):
        lrc = ""
        for lyric in lyrics:
            lrc += f"[{lyric[0]}] {lyric[1].replace("\n", "\\n")}\n"
        
        with open(self.PROJECT.lyrics_file, 'w') as f:
            f.write(lrc)
    
    def read_lrc(self):
        lyrics = []
        with open(self.PROJECT.lyrics_file, "r") as f:
            data = f.read().split("\n")[:-1]
            for item in data:
                x = int(item.split(" ")[0][1:-1])
                y = " ".join(item.split(" ")[1:]).replace("\\n", "\n")
                lyrics.append((x, y))
        return lyrics

class Editor():
    def __init__():
        