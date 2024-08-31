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
    
    # def generate_lrc(self):
    #     stamps = []
    #     total_frames = len(listdir(self.PROJECT.extracts_path))

    #     for i, frame in tqdm(enumerate(listdir(self.PROJECT.extracts_path)), desc="pasing frames..."):
    #         # skipping offset
    #         if (i < self.PROJECT.extract_offset): continue

    #         frame_path = path.join(self.PROJECT.extracts_path, frame)
    #         result = self.OCR.extract_text(frame_path)
            
    #         if (len(stamps) > 0):
    #             if (stamps[-1][1] != result): stamps.append((i, result))
    #         else:
    #             stamps.append((i, result))
    
    def generate_lrc(self):
        stamp = self.OCR.extract_pdf(self.PROJECT.extract_frames_pdf)
        return stamp