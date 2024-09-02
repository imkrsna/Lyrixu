from ext.project import Project
from ext.editor import LRC, Editor

if __name__ == "__main__":
    PROJECT = Project("./tmp/")
    lrc = LRC("https://youtu.be/wFmTntV_F_k", PROJECT)
    # lrc.download_video()
    # lrc.download_audio()
    # lrc.extract_frames()
    # lrc.generate_lyrics()
    # print(lrc.clean_lyrics(lyrics))
    editor = Editor(PROJECT)
    editor.generate_video()