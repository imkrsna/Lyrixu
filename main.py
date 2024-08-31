from ext.helper import Project
from ext.editor import LRC
from ext.ocr import OCR

PROJECT = Project(offset=60)
lrc = LRC("https://youtu.be/CBwQcZ-Boc4", PROJECT)
# lrc.download_video()
# lrc.download_audio()
lrc.extract_frames()
print(lrc.generate_lrc())

# ocr = OCR()
# print(ocr.extract_pdf())