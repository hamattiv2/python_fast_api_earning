from fastapi import FastAPI, File, UploadFile
import shutil
import pytesseract

app = FastAPI()

@app.post('/ocr')
def ocr(image: UploadFile = File(...)):
    file_path = 'txtfile'
    with open(file_path, 'w+b') as buffer:
        shutil.copyfileobj(image.file, buffer)
        
    return pytesseract.image_to_string(file_path, lang='jpn')