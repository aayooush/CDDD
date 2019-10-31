from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np
import keras
import tensorflow as tf
import cv2

# Keras
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.preprocessing import image
from tensorflow.keras.layers import Conv2D, Input
from tensorflow.keras.regularizers import l2

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()
MODEL_PATH = 'models/resnet20.h5'

print(MODEL_PATH)

# Load your trained model
model = tf.keras.models.load_model(MODEL_PATH)
model.compile(loss = 'categorical_crossentropy', 
              optimizer='rmsprop', 
              metrics=['accuracy'])
model._make_predict_function()          # Necessary
print('Model loaded. Start serving...')
# model.compile(optimizer=SGD(lr=0.01, momentum=0.9), loss="categorical_crossentropy", metrics=["acc"])

disease ={0:'Healthy', 
          1:'Mosaic_Virus', 
          2:'rust', 
          3:'woolyaphids'} 

# You can also use pretrained model from Keras
# Check https://keras.io/applications/
# from keras.applications.resnet50 import ResNet50
# model = ResNet50(weights='imagenet')
print('Model loaded. Check http://127.0.0.1:5000/')


def model_predict(img_path, model):
    
    img = image.load_img(img_path, target_size=(300, 300))
    
    batch_holder = np.zeros((1, 300,300, 3))
    
    batch_holder[0, :] = img

    # Preprocessing the image
    # x = image.img_to_array(img)
    # # x = np.true_divide(x, 255)
    # x = np.expand_dims(x, axis=0)
    # 
    # # Be careful how your trained model deals with the input
    # # otherwise, it won't make correct prediction!
    # x = preprocess_input(x, mode='caffe')
    
    preds = model.predict_classes(batch_holder)

    # preds = model.predict(img)
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

        # Process your result for human
        # pred_class = preds.argmax(axis=-1)            # Simple argmax
        # pred_class = decode_predictions(preds, top=1)   # ImageNet Decode
        # result = str(pred_class[0][0][1])               # Convert to string
        
        result = str(preds[0])
        return result
    return None


if __name__ == '__main__':
    # app.run(port=5002, debug=True)

    # Serve the app with gevent
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
