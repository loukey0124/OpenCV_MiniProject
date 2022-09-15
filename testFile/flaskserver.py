from flask import Flask, request, render_template
import os
from werkzeug.utils import secure_filename
import flaskserver    

app = Flask(__name__, static_folder='faces', template_folder='template')



if __name__ == '__main__':
    app.run(
    host="0.0.0.0",
    port=5000,
    debug=True)