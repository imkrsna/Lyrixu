from ext.project import Project
from ext.editor import LRC, Editor

if __name__ == "__main__":
    PROJECT = Project("./tmp/")
    lrc = LRC("https://www.youtube.com/watch?v=2zp1dPs-7Hk", PROJECT)
    # lrc.download_video()
    # lrc.download_audio()
    # lrc.extract_frames()
    lrc.generate_lyrics()
    # editor = Editor(PROJECT)
    # editor.generate_video()