import numpy as np
import preprocess2 as pp

from keras.models import Model
from keras.applications.inception_v3 import InceptionV3, preprocess_input, decode_predictions
from keras.preprocessing import image
from keras.optimizers import SGD
from keras.layers import Dense, GlobalAveragePooling2D, merge, Dropout
from keras.callbacks import Callback
from keras.utils.np_utils import to_categorical
from keras import backend as K
from sklearn import preprocessing


class TrainingHistory(Callback):
    # Tanulási folyamat elején létrehozunk egy-egy üres listát a kinyerni
    # kívánt metrikák tárolása céljából.

    def on_train_begin(self, logs={}):
        # Hiba mértéke a tanító adatokon.
        self.losses = []
        # Hiba mértéke a validációs adatokon.
        self.valid_losses = []
        # A modell jóságát, pontosságát mérő mutatószám a tanító adatokon.
        self.accs = []
        # A modell jóságát, pontosságát mérő mutatószám a validációs adatokon.
        self.valid_accs = []
        # A tanítási fázisok sorszámozása.
        self.epoch = 0

    # Minden egyes tanítási fázis végén mentsük el, hogy hogyan teljesít
    # aktuálisan a háló.
    def on_epoch_end(self, epoch, logs={}):
        if epoch % 1 == 0:
            self.losses.append(logs.get('loss'))
            self.valid_losses.append(logs.get('val_loss'))
            self.accs.append(logs.get('acc'))
            self.valid_accs.append(logs.get('val_acc'))
            self.epoch += 1


def prepare_data():
    # betöltjük a képeket leíró adatfájlt és a statisztikát a festők képeinek
    # eloszlásáról (előfordulás szerint növekvő lista)
    csv_data, author_stat = pp.csv_load()
    # kiválasztjuk a 100 legnépszerűbb festőt (ez az összes kép esetén kb
    # 27.000 kép)
    authors_to_select = author_stat[-100:]
    # frissítjük az adatfájlt hogy már csak a kiválaszott festők képeit töltse
    # be
    csv_data_selected = pp.csv_select(csv_data, authors_to_select)
    train_images, labels = pp.load_images(csv_data_selected)

    # kódoljuk a festőket
    encoder = preprocessing.LabelEncoder()
    encoder.fit(labels)
    labels_onehot = to_categorical(encoder.transform(labels))

    return train_images, labels_onehot, encoder


def make_model(output_layer_size):
    base_model = InceptionV3(weights='imagenet', include_top=False)

    # kinyerjük a stílusjegyeket a cnn köztes rétegegeiből (és max pool cnn
    # kimeneti rétegére)
    desired_layers = [28, 44, 60, 70, 92, 114, 136, 158, 172, 194]
    style_layers = [None] * len(desired_layers)

    for i in range(len(desired_layers)):
        style_layers[i] = base_model.layers[desired_layers[i]].output
        style_layers[i] = GlobalAveragePooling2D()(style_layers[i])
        style_layers[i] = Dense(base_model.layers[desired_layers[i]].output_shape[
                                3], activation='relu')(style_layers[i])

    # egymás mellé tesszük a különböző szintű feature-öket
    ff = merge(style_layers, mode='concat')

    # ezután hozzáadunk két előrecsatolt réteget ReLU aktivációs függvénnyel
    ff = Dense(2048, activation='relu')(ff)
    ff = Dropout(0.5)(ff)
    ff = Dense(1024, activation='relu')(ff)

    # és végül egy kimenete lesz a hálónak - a "binary_crossentropy"
    # költségfüggvénynek erre van szüksége
    predictions = Dense(output_layer_size, activation='softmax')(ff)

    # a model létrehozása
    return base_model, Model(input=base_model.input, output=predictions)


def learn():
    train_images, labels_onehot, encoder = prepare_data()
    base_model, model = make_model(output_layer_size=labels_onehot.shape[1])
    history = TrainingHistory()

    # két lépésben fogjuk tanítani a hálót
    # az első lépésben csak az előrecsatolt rétegeket tanítjuk, a konvolúciós
    # rétegeket befagyasztjuk
    for layer in base_model.layers:
        layer.trainable = False
    # lefordítjuk a modelt (fontos, hogy ezt a rétegek befagyasztása után csináljuk"
    # mivel két osztályunk van, ezért bináris keresztentrópia költségfüggvényt
    # használunk
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(train_images, labels_onehot, batch_size=16,
              nb_epoch=50, validation_split=0.2, callbacks=[history])

    # és ismét indítunk egy tanítást, ezúttal nem csak az előrecsatolt rétegek,
    # hanem az Inception V3 felső rétegei is tovább tanulnak
    for layer in model.layers[172:]:
        layer.trainable = True
    # ez után újra le kell fordítanunk a hálót, hogy most már az Inception V3
    # felsőbb rétegei tanuljanak
    model.compile(optimizer=SGD(lr=0.0001, momentum=0.9),
                  loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(train_images, labels_onehot,  batch_size=32,
              nb_epoch=100, validation_split=0.2, callbacks=[history])

    print("Tanítás vége.")

if __name__ == "__main__":
    learn()
