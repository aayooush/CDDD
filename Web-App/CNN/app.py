from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np

# Keras
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

import tensorflow as tf
import cv2
import numpy as np
# import matplotlib.pyplot as plt
# from tensorflow.keras.models import load_model

IMG_W = 224
IMG_H = 224
disease ={0:'Healthy', 
          1:'Rust', 
          2:'Wooly Aphids', 
          3:'Mosaic Virus'} 

def normalize(df):    
    return (df - df.min()) / (df.max() - df.min())

def process(path):
    im = cv2.imread(path, cv2.IMREAD_COLOR) 
    b,g,r = cv2.split(im)
    image = cv2.merge([r,g,b])
    res = cv2.resize(image,(IMG_W, IMG_H), interpolation = cv2.INTER_CUBIC)
    return np.array(res, dtype=np.int32)

# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()
MODEL_PATH = 'models/CNN-Model-New.h5'

# Load your trained model
model = tf.keras.models.load_model(MODEL_PATH)
model.compile(loss="categorical_crossentropy", optimizer='sgd', metrics=["accuracy"])
model._make_predict_function()          # Necessary

# model = joblib.load(MODEL_PATH)

print('Model loaded. Start serving...')

# You can also use pretrained model from Keras
# Check https://keras.io/applications/
# from keras.applications.resnet50 import ResNet50
# model = ResNet50(weights='imagenet')
print('Model loaded. Check http://127.0.0.1:5000/')


def model_predict(img_path, model):

    # img = image.load_img(img_path, target_size=(200, 200))
    # 
    # # Preprocessing the image
    # x = image.img_to_array(img)
    # # x = np.true_divide(x, 255)
    # x = np.expand_dims(x, axis=0)
    # 
    # # Be careful how your trained model deals with the input
    # # otherwise, it won't make correct prediction!
    # x = preprocess_input(x, mode='caffe')
    # 
    # preds = model.predict(x)
    img = process(img_path)

    input_image = []
    input_image.append(normalize(img))
    input_image = np.array(input_image)
    preds = model.predict(input_image)
    
    return preds


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['image']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)
        
        fp = []
        for i in preds:
            fp.append(list(i).index(max(i)))
            
        result = disease[fp[0]]

        # Process your result for human
        
        # result = list(preds).index(max(preds))
        return result
    return None


if __name__ == '__main__':
    # app.run(port=5002, debug=True)

    # Serve the app with gevent
    http_server = WSGIServer(('192.168.43.217',5000),app)
    http_server.serve_forever()
