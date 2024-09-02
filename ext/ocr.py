import json
import requests

class OCR:
    def __init__(self):
        self.api = None
        self.url = r"https://api.ocr.space/parse/image"
        self.load_api()
    
    def load_api(self):
        # reading config file
        with open("config.json", "r") as f:
            config = json.load(f)

        # reading all api keys file
        with open("api.json", "r") as f:
            data = json.load(f)
            temp = (int(config["api_last"]) + 1) % len(data["keys"])
            self.api = data["keys"][temp]
            config["api_last"] = (int(config["api_last"]) + 1)

        # upading config file
        with open("config.json", "w") as f:
            json.dump(config, f)
    
    def extract_text(self, pdf_path: str):
        # setting up meta data
        headers = {"apikey": self.api}
        payload = {"OCREngine": 2}
        files = [('file', open(pdf_path, 'rb'))]

        # acessing api
        response = requests.post(url=self.url, headers=headers, data=payload, files=files)
        data = response.json()

        # taking out parsed text
        # raw_lyrics = {}
        raw_lyrics = []
        
        for i, text in enumerate(data["ParsedResults"]):
            # raw_lyrics[i] = text["ParsedText"]
            raw_lyrics.append(text["ParsedText"])
        
        # returning raw lyrics
        return raw_lyrics