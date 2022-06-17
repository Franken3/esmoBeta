import time

import numpy as np
from flask import jsonify

import face_recognition


def compare_two_faces(file1, file2):
    start_time = time.time()
    image_one = np.array(file1.convert('RGB'))
    image_two = np.array(file2.convert('RGB'))
    pre_res_file_one, pre_res_file_two = True, True
    try:
        image_one_encoding = face_recognition.face_encodings(image_one)[0]
    except:
        pre_res_file_one = False
    try:
        image_two_encoding = face_recognition.face_encodings(image_two)[0]
    except:
        pre_res_file_two = False

    # See how far apart the test image is from the known faces

    if pre_res_file_one and pre_res_file_two:
        face_distances = face_recognition.face_distance([image_one_encoding], image_two_encoding)
        res = {"percent": (1 - face_distances[0]) * 100,
               "calc_time": (" %s seconds " % (time.time() - start_time)),
               "serv_time": time.time()
               }
    else:
        res = {"percent": "error",
               "first_img": 1 if pre_res_file_one else 0,
               "second_img": 1 if pre_res_file_two else 0
               }
    print(res)
    return jsonify(res)
