from flask import Flask, request, render_template
import os
import cv2 as cv
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def method():
    return 'nodata'

upload_path = "./data"
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = secure_filename(file.filename)
    os.makedirs(upload_path, exist_ok=True)
    file.save(os.path.join(upload_path, filename))
    return 'Upload Success'

if __name__ == '__main__':
    app.run(
    host="0.0.0.0",
    port=5000,
    debug=True)