import os
import json
import numpy as np

import base64
from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from keras.models import Model, model_from_json
from keras.applications.inception_v3 import InceptionV3
from keras.layers import Dense, GlobalAveragePooling2D, merge, Dropout
from keras.utils.np_utils import to_categorical
from keras.preprocessing import image

import tensorflow as tf
tf.python.control_flow_ops = tf

UPLOAD_FOLDER = './images'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png'])

#Creating the webservice
app = Flask(__name__)
#Setting the upload folder for the webservice
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#variable holding the exported kerasjs model
model = None


# FLASK IMAGE UPLOAD SCRIPT FROM
# http://flask.pocoo.org/docs/0.11/patterns/fileuploads/

#Checking whether the uploaded image has allowed extensiom
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

#returning/displaying an uploaded file by name
@app.route('/images/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

#Defining route for our main webservice
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    #In case of POST HTTP call
    if request.method == 'POST':
        #In case the upload is not successful
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        #In case the upload was successful: moving the image to the server and also preprocessing it for input
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #preprocess the image for network input
            small_image_array = preprocess_image(filename)
            #Invokeing the network
            output = predict(model, small_image_array)
            return json.dumps(output)
    return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form action="" method=post enctype=multipart/form-data>
          <p><input type=file name=file>
             <input type=submit value=Upload>
        </form>
        '''

#Loading the exported model
def load_model():
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    #Loading the exported weights
    model.load_weights('sulyok.hdf5')
    return model


def predict(model, image):
    output = model.predict(x=[image], batch_size=1, verbose=0)
    output = output[0]
    output2 = []
    for i in range(len(output)):
        output2.append([output[i], i])
    output2.sort(key=lambda x: x[0])
    output2 = output2[::-1]
    for i in range(len(output2)):
        output2[i][0] = str(output2[i][0])
        output2[i][1] = str(output2[i][1])
    return output2

#Preprocessing the image
def preprocess_image(img_name):
    file_name, ext = os.path.splitext(img_name)
    #Resizing the target image for size 256x256
    small_image = image.load_img(
        '.' + url_for('uploaded_file', filename=img_name), target_size=(256, 256))
    #saving the small image later used as input
    small_image.save('./images/' + file_name + '_thumbnail.jpg', 'JPEG')
    #transforming the image to tensors
    small_image_array = np.array(small_image)
    small_image_array = small_image_array[None, :]
    return small_image_array

#Initializing the service and invokeing the newtwork model load
if __name__ == "__main__":
    model = load_model()
    app.run()
