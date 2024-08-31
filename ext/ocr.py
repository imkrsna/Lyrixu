import json
import requests

class OCR():
    def __init__(self):
        self.api = None
        self.url = r"https://api.ocr.space/parse/image"
        self.load_api()

    def load_api(self):
        with open("api.json", "r") as f:
            data = json.load(f)
            self.api = data["keys"][1]

    def extract_text(self, frame: str):
        headers = {"apikey": self.api}
        payload = {"OCREngine": 2}
        files = [('file', open(frame, 'rb'))]
        response = requests.post(self.url, files=files, headers=headers, data=payload)
    
        data = response.json()
        print(data)
        if (int(data["OCRExitCode"]) < 3):
            text = []
            for i in data["ParsedResults"]:
                text.append(i["ParsedText"].replace(r"\r", ""))
            
            return "\n".join(text)
        else:
            return None
    
    def extract_pdf(self, pdf_path):
        # setting up meta data for request
        headers = {"apikey": self.api}
        payload = {"OCREngine": 2}
        files = [('file', open(pdf_path, 'rb'))]
    
        # getting data from api
        response = requests.post(self.url, files=files, headers=headers, data=payload)
        data = response.json()
        
        
        # extracting text from data
        stamp = []
        for i, text in enumerate(data["ParsedResults"]):
            stamp.append((i, text["ParsedText"]))
        
        return stamp