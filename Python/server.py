import os
from app import app
import cv2
from colorget import getScheme
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template, jsonify
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableDict

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@cross_origin()
@app.route('/upload', methods=['POST'])
def upload_image():
	file = request.files["file"]
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join("./uploads", secure_filename(filename)))
		result = getScheme("./uploads/"+filename)
		return jsonify(result)
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return

if __name__ == "__main__":
    app.run()