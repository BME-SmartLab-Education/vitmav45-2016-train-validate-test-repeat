import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import send_from_directory
from keras.models import Model
from keras.applications.inception_v3 import InceptionV3
from keras.layers import Dense, GlobalAveragePooling2D, merge, Dropout
import numpy as np
from keras.utils.np_utils import to_categorical


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
            small_image = preprocess_image(uploaded_file(filename))
            output = predict(model, small_image)
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
    base_model = InceptionV3(weights='imagenet', include_top=False)

    # kinyerjük a stílusjegyeket a cnn köztes rétegegeiből (és max pool cnn
    # kimeneti rétegére)
    desired_layers = [28, 44, 60, 70, 92, 114, 136, 158, 172, 194]
    style_layers = [None] * len(desired_layers)

    for i in range(len(desired_layers)):
        style_layers[i] = base_model.layers[desired_layers[i]].output
        style_layers[i] = GlobalAveragePooling2D()(style_layers[i])
        style_layers[i] = Dense(base_model.layers[desired_layers[i]].output_shape[3], activation='relu')(style_layers[i])

    # egymás mellé tesszük a különböző szintű feature-öket
    ff = merge(style_layers, mode='concat')

    # ezután hozzáadunk két előrecsatolt réteget ReLU aktivációs függvénnyel
    ff = Dense(2048, activation='relu')(ff)
    ff = Dropout(0.5)(ff)
    ff = Dense(1024, activation='relu')(ff)

    # és végül egy kimenete lesz a hálónak - a "binary_crossentropy" költségfüggvénynek erre van szüksége
    # 10 az output_layer_size
    predictions = Dense(10, activation='softmax')(ff)

    # a model létrehozása
    model = Model(input=base_model.input, output=predictions)

    # #################
    # TODO súlybetöltés
    # #################

    model.load_weights(None)

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
