from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from waitress import serve 
from PIL import Image
from keras.models import load_model
import numpy as np
from object_classes import *
import cv2
import tensorflow as tf
from PIL.Image import Resampling

# Khởi tạo Flask
app = Flask(__name__)
CORS(app)

def sort_results(predictions):
    # convert the predictions to a list of dictionaries
    top = [{'probability': float(p), 'className': IMAGENET_CLASSES[i]} for i, p in enumerate(predictions[0])]
    # sort the predictions by probability in descending order
    top = sorted(top, key=lambda x: x['probability'], reverse=True)
    return top

@app.route("/", methods=['GET'])
def home_page():
    return render_template('index.html')

# define a route for the API
@app.route('/classify', methods=['POST'])
def predict():
    # parse the image data from the request
    image = Image.open(request.files['image'].stream)

    image = image.convert('RGB')

    # preprocess the image data
    image = image.resize((224, 224), resample=Resampling.NEAREST) # example resizing
    image = np.array(image) / 255.0 # example normalization
    image = image[:, :, :3]

    # Add a batch dimension to the image
    image = np.expand_dims(image, axis=0)

    # load the model and perform inference
    model = load_model('../models/resnet.h5') # replace with your own model loading code
    
    # result = model.predict(np.expand_dims(image, axis=0))
    result = model.predict(image)
    
    top = sort_results(result)

    # return the output as a JSON response
    return jsonify({'top1': top[0], 'top2': top[1]})


if __name__ == '__main__':
    # app.run(host='0.0.0.0', debug=False)
    serve(app, host='0.0.0.0', port=5000)
