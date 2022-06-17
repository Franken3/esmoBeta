import base64
import time
from io import BytesIO

import numpy as np
from PIL import Image
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

import face_recognition
from worker_compare import compare_two_faces

app = Flask(__name__)
cors = CORS(app)

@app.route('/', methods=['GET', 'POST'])
@cross_origin()
def upload_image():
    # Check if a valid image file was uploaded
    print("------")
    if request.method == 'POST':
        print(repr(request.content_type))
        print(request.data)
        content = request.get_json()
        print(content)
        try:
            file1 = Image.open(BytesIO(base64.b64decode(content['file1']))).convert('RGB')
        except:
            file1 = False
        try:
            file2 = Image.open(BytesIO(base64.b64decode(content['file2']))).convert('RGB')
        except:
            file2 = False
        if file1 and file2:
            return compare_two_faces(file1, file2)
        else:
            return 'ERROR: Не все изображения загруженны'
    return '''
    <!doctype html>
    <title>Сравнение</title>
    <h1>Загрузи 2 фотографии и получи их сходство</h1>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file1">
      <input type="file" name="file2">
      <input type="submit" value="Upload">
    </form>
    '''


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
