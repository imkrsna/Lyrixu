from ext.project import Project
from ext.editor import LRC

lyrics = {
    0: "'CAUSE IT FEELS LIKE HEAVEN\nWHEN IT HURTS SO BAD",
    1: "'CAUSE IT FEELS LIKE HEAVEN\nWHEN IT HURTS SO BAD",
    2: "'CAUSE IT FEELS LIKE HEAVEN\nWHEN IT HURTS SO BAD",
    3: "'CAUSE IT FEELS LIKE HEAVEN\nWHEN IT HURTS SO BAD",
    4: "'CAUSE IT FEELS LIKE HEAVEN\nWHEN IT HURTS SO BAD",
    5: "'CAUSE IT FEELS LIKE HEAVEN\nWHEN IT HURTS SO BAD",
    6: "'CAUSE IT FEELS LIKE HEAVEN\nWHEN IT HURTS SO BAD",
    7: "BABY, PUT IT ON ME\nI LIKE IT JUST LIKE THAT",
}

if __name__ == "__main__":
    lrc = LRC("https://youtu.be/wFmTntV_F_k", Project("./tmp/"))
    # lrc.download_video()
    # lrc.download_audio()
    # lrc.extract_frames()
    # print(lrc.generate_lyrics())
    print(lrc.clean_lyrics(lyrics))