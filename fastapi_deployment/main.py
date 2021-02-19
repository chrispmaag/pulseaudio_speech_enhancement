from fastapi import FastAPI, File, UploadFile, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from utilities import spectrogram
import shutil

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Loads the main page from welcome.html
@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request})

@app.post("/result/")
async def create_upload_file(request: Request, file: UploadFile = File(...)):
    filename = file.filename
    print(filename)
    content_type = file.content_type
    print(content_type)
    uploaded_file = file.file
    # testing default to see if it works with the librosa built in example
    # then will switch it over to try to read the file we are uploading
    # Create the noisy spectrogram
    # Let's see if passing in the file like this works
    # https://levelup.gitconnected.com/how-to-save-uploaded-files-in-fastapi-90786851f1d3
    # file.file is the Python file object
    spectrogram.create_spectrogram(file.file, audio_type="noisy")
    # Then create the enhanced spectrogram after the model processes the input file

    # Can come back to this
    # trying out shutil to save file so I can figure out a way to pass it
    # with open(f"./sound_clips/{filename}", "wb") as buffer:
        # shutil.copyfileobj(file.file, buffer)
    # file.save('/tmp/', filename)

    return templates.TemplateResponse("result.html",
                                      {"request": request, "filename": filename,
                                      "content_type": content_type}) #,
                                       # "uploaded_file": uploaded_file})

# # trying a new version of /files/ that returns a template response
# @app.post("/files/")
# async def create_file(request: Request, file: bytes = File(...)):
#     file_size = len(file)
#     file_type = type(file)
#     print(file_size)
#     print(file_type)
#     return templates.TemplateResponse("result.html",
#                                       {"request": request, "file_size": file_size,
#                                        "file_type": file_type})

# @app.get("/items/{id}", response_class=HTMLResponse)
# async def read_item(request: Request, id: str):
#     return templates.TemplateResponse("item.html", {"request": request, "id": id})

# holding area
# @app.post("/files/")
# async def create_file(file: bytes = File(...)):
#     return {"file_size": len(file)}


# @app.post("/uploadfile/")
# async def create_upload_file(file: UploadFile = File(...)):
#     return {"filename": file.filename}

# @app.get("/result/", response_class=HTMLResponse)
# async def read_item(request: Request):
#     return templates.TemplateResponse("result.html", {"request": request})
