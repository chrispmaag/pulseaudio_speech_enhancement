from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from denoiser.enhance import enhance

import spectrogram
import uuid
import os

app = Flask(__name__)

@app.route('/')
def main():
    """[summary]

    Returns:
        [type]: [description]
    """
    return render_template('welcome.html')

@app.route('/results', methods=['POST'])
def upload_file():
    """[summary]

    Returns:
        [type]: [description]
    """
    if request.method == 'POST':
        
        # TODO: Add file format validations!!

        request_id = str(uuid.uuid4())

        file = request.files['file']
        file.save(f'./static/{request_id}.wav')

        enhance(model_path='./denoiser/best.th',
                noisy_dir='/tmp/',
                file_location=f'./static/{request_id}.wav',
                out_dir='./static/',
                noisy_json=None,
                sample_rate=16000,
                batch_size=1,
                device='cpu',
                num_workers=10,
                dns48=False,
                dns64=False,
                master64=False,
                dry=0,
                streaming=False,
                verbose=20)

        spectrogram.create_spectrogram(request_id, audio_type='noisy')
        spectrogram.create_spectrogram(request_id, audio_type='enhanced')

        return render_template('result.html', request_id=request_id)

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

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
