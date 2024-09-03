import re
import json
from os import path, listdir
from PIL import Image
from ext.ocr import OCR
from pytubefix import YouTube
from ext.project import Project
from pytubefix.cli import on_progress
from moviepy.editor import VideoFileClip, ImageClip, TextClip, CompositeVideoClip, AudioFileClip
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout

class LRC:
    def __init__(self, url: str, PROJECT: Project):
        # base project
        self.PROJECT = PROJECT
        self.ocr = OCR()

        # video variables
        self.url = url
        self.video = YouTube(url=url, on_progress_callback=on_progress)
        self.duration = None

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
        
        # cleaning lyrics
        raw_lyrics = self.clean_lyrics(raw_lyrics)

        audio = AudioFileClip(self.PROJECT.input_audio)
        self.duration = audio.duration

        # saving lyrics file
        with open(self.PROJECT.lyrics_file, "w") as f:
            json.dump(raw_lyrics, f)
        
        # convering lyrics dict to tupile list
        flag = False
        last = None
        processed_lyrics = []
        for item in list(raw_lyrics.items())[::-1]:
            if (flag):
                processed_lyrics.append((item[1], int(item[0]), int(last[0])))
                last = item
            else:
                processed_lyrics.append((item[1], int(item[0]), self.duration))
                last = item
                flag = True
        
        processed_lyrics = processed_lyrics[::-1]

        # saving str file
        srt = ""
        for idx, item in enumerate(processed_lyrics):
            srt += f"{idx}\n{self.timestamp(item[1])} --> {self.timestamp(item[2])}\n{item[0]}\n\n"
        
        with open(self.PROJECT.srt_file, "w") as f:
            f.write(srt)

    def timestamp(self, seconds: float):
        seconds = int(seconds)
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = (seconds % 3600) % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d},000"

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
        
        # list to dict
        lyrics_dict = {}
        for item in new_lyrics:
            lyrics_dict[item[0]] = item[1]

        return lyrics_dict


class Editor:
    def __init__(self, PROJECT: Project):
        self.PROJECT = PROJECT

        # fonts
        self.font = "./data/fonts/Ouders Regular Regular.ttf"

        # audio
        self.audio = AudioFileClip(self.PROJECT.input_audio)
        
        # duration from audio
        self.duration = self.audio.duration
        
        # background
        self.background = ImageClip(self.get_background()).set_duration(self.duration)
    
    def get_background(self):
        return "./data/backgrounds/temp.jpg"
    
    def get_lyrics(self):
        # reading lyrics file
        lyrics = {}
        with open(self.PROJECT.lyrics_file, "r") as f:
            lyrics = json.load(f)

        # convering lyrics json to tupile list
        flag = False
        last = None
        processed_lyrics = []
        for item in list(lyrics.items())[::-1]:
            if (flag):
                processed_lyrics.append((item[1], int(item[0]), int(last[0])))
                last = item
            else:
                processed_lyrics.append((item[1], int(item[0]), self.duration))
                last = item
                flag = True
        
        return processed_lyrics[::-1]


    def generate_video(self):
        # getting lyrics
        lyrics = self.get_lyrics()

        text_clips = []
        for text, start_time, end_time in lyrics:
            if text == "": continue
            
            # creating new text clip
            text_clip = TextClip(text, font=self.font, fontsize=20, color="white")
            
            # calculating center position
            v_w, v_h = self.background.size
            t_w, t_h = text_clip.size
            center_x = (v_w - t_w) // 2
            center_y = (v_h - t_h) // 2

            # setting properties
            text_clip = text_clip.set_position((center_x, center_y))
            text_clip = text_clip.set_duration(end_time - start_time)
            text_clip = text_clip.crossfadein(duration=0.5)
            text_clip = text_clip.crossfadeout(duration=0.5)
            text_clip = text_clip.set_start(start_time).set_end(end_time)
            text_clips.append(text_clip)
        

        video = CompositeVideoClip([self.background] + text_clips)
        video = video.set_audio(self.audio)
        video.write_videofile(self.PROJECT.render_file, audio=True, fps=24, threads=4, codec="libx264")