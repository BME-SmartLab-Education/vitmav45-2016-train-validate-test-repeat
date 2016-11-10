import csv
import os
import gc
import operator
import numpy as np
from collections import defaultdict
from keras.preprocessing import image

def csv_load(csv_file_name = "train_info_modified_fixed.csv"):
    csv_data = {}
    author_stat = defaultdict(int)

    with open(csv_file_name) as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        for line in reader:
            csv_data[line[0]] = line[1:]
            author_stat[line[1]] += 1

    return csv_data, sorted(author_stat.items(), key=operator.itemgetter(1))


def csv_select(sorce_csv_data, target_authors):
    return { name: data for name, data in sorce_csv_data.items() if data[0] in target_authors }


def load_images(csv_data, location = "train_sample"):
    # TODO: limit lehetőséget hozzáadni!
    data = []
    labels = []
    
    for subdir, dirs, files in os.walk(location):
        for file in files:
            if file in csv_data:
                img_loc = os.path.join(subdir, file)
                img = image.load_img(img_loc, target_size=(256, 256))
                labels.append(csv_data[file][0])
                img_arr = np.array(img) # TODO: dtype="uint8" - de lehet hogy gond lesz a kerassal, pl standardizálás
                data.append(img_arr)
                
                img_loc = None
                img = None
                img_arr = None

                if len(labels) % 2000 == 0:
                    print(len(labels), "images loaded")

                if len(labels) % 10 == 0: # ezt meg kellene próbálni növelni akár 2000-ig
                    print("GC collect: ", gc.collect())

    np_data = np.array(data)
    np_labels = np.array(labels)

    # takarítás...
    data = None
    labels = None
    gc.collect()

    return np_data, np_labels


if __name__ == "__main__":
    print()

    csv_data = csv_load()
    images, labels = load_images(csv_data)
