from os import path, makedirs

class Project:
    def __init__(self, project_path: str = "./tmp/"):
        # base paths
        self.project_path = project_path
        
        # folder paths
        self.downloads_path = path.join(project_path, "downloads/")
        self.extracts_path = path.join(project_path, "extracts/")
        self.exports_path = path.join(project_path, "exports/")
        self.render_path = path.join(self.downloads_path, "render/")

        # file paths
        self.input_video_name = "input.mp4"
        self.input_video = path.join(self.downloads_path, self.input_video_name)
        self.input_audio_name = "input.mp3"
        self.input_audio = path.join(self.downloads_path, self.input_audio_name)
        self.input_frames = path.join(self.extracts_path, "frame_{0:08d}.jpg")
        self.output_frames = path.join(self.render_path, "frame_{0:08d}.jpg")
        self.frames_pdf = path.join(self.extracts_path, "frames_{0:04d}.pdf")
        self.lyrics_file = path.join(self.exports_path, "lyrics.json")
        self.srt_file = path.join(self.exports_path, "lyrics.srt")
        self.render_file = path.join(self.exports_path, "render.mp4")

        # making folders
        makedirs(self.downloads_path, exist_ok=True)
        makedirs(self.extracts_path, exist_ok=True)
        makedirs(self.exports_path, exist_ok=True)
        makedirs(self.render_path, exist_ok=True)

        # input variables
        self.input_fps = 1
        self.input_margin = 80
        self.input_stack = 819200 # 800 * 1024