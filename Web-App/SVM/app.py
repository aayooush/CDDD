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

from sklearn.externals import joblib
import skimage
from skimage.io import imread
from skimage.transform import resize
from sklearn.utils import Bunch

label_output = ['Healthy', 'Mosiac_Virus', "Wooly Aphids", "Rust"]

def load_image_file(file, dimension=(128, 128)):
    images = []
    flat_data = []
    target = []
 
    img = skimage.io.imread(file)
    img_resized = resize(img, dimension, anti_aliasing=True, mode='reflect')
    flat_data.append(img_resized.flatten()) 

    flat_data = np.array(flat_data)

    return Bunch(data=flat_data,)

# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()
MODEL_PATH = 'models/SVM_SKLEARN.sav'

# Load your trained model
# model = load_model(MODEL_PATH)
# model._make_predict_function()          # Necessary

model = joblib.load(MODEL_PATH)

print('Model loaded. Start serving...')

# You can also use pretrained model from Keras
# Check https://keras.io/applications/
# from keras.applications.resnet50 import ResNet50
# model = ResNet50(weights='imagenet')
print('Model loaded. Check http://127.0.0.1:5000/')


def model_predict(img_path, model):

    x = img_path
    input_image = load_image_file(x)
    result = model.predict(input_image.data)[0]
    return label_output[result]


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
        
        result = preds
        return result
    return None


if __name__ == '__main__':
    # app.run(port=5002, debug=True)

    # Serve the app with gevent
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
