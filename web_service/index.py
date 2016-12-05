import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import send_from_directory
from keras.models import Model, model_from_json
from keras.applications.inception_v3 import InceptionV3
from keras.layers import Dense, GlobalAveragePooling2D, merge, Dropout
import numpy as np
from keras.utils.np_utils import to_categorical
import json


from keras.preprocessing import image

UPLOAD_FOLDER = './images'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# FLASK IMAGE UPLOAD SCRIPT FROM
# http://flask.pocoo.org/docs/0.11/patterns/fileuploads/


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/images/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            model = load_model()
            # small_image = preprocess_image(uploaded_file(filename))
            # output = predict(model, small_image)
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


def load_model():
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(json.loads(loaded_model_json))
    model.load_weights('sulyok.hdf5')
    return model


def predict(model, image):
    output = model.predict(x=image, batch_size=1, verbose=0)

    # #################
    # TODO kimenetn rendezés
    # #################

    return output


def preprocess_image(image):

    # #################
    # TODO méretezés és arrayre változtatás
    # #################

    small_image = None

    return small_image

if __name__ == "__main__":
    app.run()
