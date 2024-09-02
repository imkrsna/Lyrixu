import re
from os import path, listdir
from PIL import Image
from ext.ocr import OCR
from pytubefix import YouTube
from ext.project import Project
from pytubefix.cli import on_progress
from moviepy.editor import VideoFileClip

class LRC:
    def __init__(self, url: str, PROJECT: Project):
        # base project
        self.PROJECT = PROJECT
        self.ocr = OCR()

        # video variables
        self.url = url
        self.video = YouTube(url=url, on_progress_callback=on_progress)

    def download_video(self):
        stream = self.video.streams.get_highest_resolution()
        stream.download(output_path=self.PROJECT.downloads_path, filename=self.PROJECT.input_video_name)

    def download_audio(self):
        stream = self.video.streams.get_audio_only()
        stream.download(output_path=self.PROJECT.downloads_path, filename=self.PROJECT.input_audio_name)
    
    def extract_frames(self):
        # loading input video
        clip = VideoFileClip(self.PROJECT.input_video)
        
        # pdf set counter
        counter = 1
        counter_size = 0
        images = {}

        # looping and storing frames
        for i, frame in enumerate(clip.iter_frames(fps=self.PROJECT.input_fps)):
            if (counter_size >= self.PROJECT.input_stack):
                counter += 1
                counter_size = 0

            # making pillow image from frame
            image = Image.fromarray(frame)
            width, height, margin = image.width, image.height, self.PROJECT.input_margin
            
            # cropping top and bottom for better readiblity
            image = image.crop((0, margin, width, height - margin))
            
            # saving frame
            image.save(self.PROJECT.input_frames.format(i))

            # calculating images size so far
            counter_size += path.getsize(self.PROJECT.input_frames.format(i))

            # appending pdf page
            try:
                images[counter].append(image)
            except KeyError:
                images[counter] = [image]

        
        # making frames.pdf
        for i in images.keys():
            images[i][0].save(self.PROJECT.frames_pdf.format(i), save_all=True, append_images=images[i][1:])
    
    def generate_lyrics(self):
        frame_files = re.findall("frames_[0-9]{4}.pdf", "\n".join(listdir(self.PROJECT.extracts_path)))
        frame_files.sort() # safety sorting
        
        # creating raw_lyrics dict and file counter
        raw_lyrics = {}
        counter = 0

        # looping throught returned result and filling raw_lyrics
        for i, file in enumerate(frame_files):
            lyrics = self.ocr.extract_text(self.PROJECT.frames_pdf.format(i+1))
            for text in lyrics:
                raw_lyrics[counter] = text
                counter += 1
        # raw_lyrics = self.ocr.extract_text(self.PROJECT.frames_pdf)
        return raw_lyrics

    def clean_lyrics(self, lyrics: dict):
        new_lyrics = []
        flag = False # stop check on first element
        
        for (i, text) in lyrics.items():
            if flag:
                if new_lyrics[-1][-1] != text:
                    new_lyrics.append((i, text))
            else:
                new_lyrics.append((i, text))
                flag = True
        
        # returning clean lyrics
        return new_lyrics
            