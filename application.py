# Importing Dependencies
import json
import base64
import numpy as np
from flask_restful import Resource, Api
from flask import Flask, request, jsonify, make_response
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.inception_v3 import preprocess_input

# APP Setup
application = app = Flask(__name__)
api = Api(application)
my_model = load_model("inception_v3_299x299.model")

# Helper Functions

# Function to decode from base64


def decode_from_base64(data):
    return base64.b64decode(data)

# Function to save the image and get prediction using the func_predict


def save_and_predict(data):
    Default_File = 'default.jpg'
    with open(Default_File, 'wb') as f:
        f.write(data)
    prediction = func_predict(Default_File)
    return prediction

# Function to predict using inception model


def func_predict(image_path):
    image_file = image.load_img(image_path, target_size=(299, 299))
    image_array = image.img_to_array(image_file)
    image_array = np.expand_dims(image_array, axis=0)
    img = preprocess_input(image_array)
    prediction = my_model.predict(img)
    if prediction[0][0] < 0.5:
        return ("Cat")
    else:
        return ("Dog")

# API


class Predict_API(Resource):
    # POST request
    def post(self):
        json_data = request.get_json(force=True)
        input_list = json_data['input_list']  # input list of API
        output_list = []  # output list of API
        if len(input_list) != 0:
            for image_data in input_list:

                if len(image_data) != 0:
                    try:
                        imgdata = decode_from_base64(image_data)
                    except:  # if there is a error with the base64 string
                        return make_response(jsonify({"ValueError": "Cannot decode from base64"}), 400)
                    prediction = save_and_predict(imgdata)
                    # appending prediction to output list
                    output_list.append(prediction)

                else:  # if len(image_data) != 0
                    return make_response(jsonify({"Error": "Image not recieved"}), 400)

            return make_response(jsonify({"predictions": output_list}), 200)

        else:  # if len(input_list) != 0
            return make_response(jsonify({"Error": "Image data not present"}), 400)
# GET request

    def get(self):
        return make_response(jsonify({"info": "Api is working, use the post request to make predictions."}), 200)


# add Predict_API class to application
api.add_resource(Predict_API, '/')
if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)
