from ext.editor import Editor

PROJECT_PATH = "./"
editor = Editor("https://youtu.be/q7mlB-adMBc", PROJECT_PATH, fps=0.5)
editor.download_video()
editor.extract_frames()