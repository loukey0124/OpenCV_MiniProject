from flask import Flask, request, render_template
import os
from werkzeug.utils import secure_filename
import cv2

app = Flask(__name__,static_folder='static',template_folder='template')

upload_path = './data'
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = secure_filename(file.filename)
    os.makedirs(upload_path, exist_ok=True)
    file.save(os.path.join(upload_path, filename))
    imageFile = os.path.join(upload_path, filename)
    #사진 띄우기
    img  = cv2.imread(imageFile)    # cv2.IMREAD_COLOR
    cv2.imshow('Camera Image',img)
    cv2.waitKey(6000)
    cv2.destroyAllWindows()
    return 'Upload Success'


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True)
