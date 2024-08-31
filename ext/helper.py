from os import path, makedirs

class Project:
    def __init__(self, name: str = "Untitled", project_path: str = "./tmp/", offset: int = 0):
        self.name = name
        self.project_path = project_path
        self.downloads_path = path.join(project_path, "downloads/")
        self.extracts_path = path.join(project_path, "extracts/")
        self.exports_path = path.join(project_path, "exports/")

        self.input_video = "input.mp4"
        self.input_audio = "input.mp3"
        self.extract_fps = 0.75
        self.extract_offset = offset

        self.extract_crop = 80

        self.input_video_path = path.join(self.downloads_path, self.input_video)
        self.input_audio_path = path.join(self.downloads_path, self.input_audio)
        self.extract_frames = path.join(self.extracts_path, "frame_{0:06d}.jpg")
        self.extract_frames_pdf = path.join(self.extracts_path, "frames.pdf") # TESTING
        self.lyrics_file = path.join(self.exports_path, "lyrics.json")
        self.render_file = path.join(self.exports_path, "render.mp4")

        makedirs(self.downloads_path, exist_ok=True)
        makedirs(self.extracts_path, exist_ok=True)
        makedirs(self.exports_path, exist_ok=True)