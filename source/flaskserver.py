from flask import Flask, request
import os
import cv2 as cv
from werkzeug.utils import secure_filename
import searchface

model = searchface.GetModel()
app = Flask(__name__)

upload_path = "./data"
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = secure_filename(file.filename)
    os.makedirs(upload_path, exist_ok=True)
    file.save(os.path.join(upload_path, filename))
    return 'Upload Success'

@app.route('/confirmFace')
def confirm():
    accuracy = searchface.ImageMatching(model)
    return str(accuracy)

if __name__ == '__main__':
    searchface.learnFace()
    app.run(
    host="0.0.0.0",
    port=5000,
    debug=True)