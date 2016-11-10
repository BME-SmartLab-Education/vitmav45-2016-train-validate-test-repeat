import csv
import os
import gc
from collections import defaultdict

import numpy as np
from keras.preprocessing import image

def csv_load(csv_file_name = "train_info_modified_fixed.csv"):
    csv_data = {}
    author_stat = defaultdict(int)

    try:
        with open(csv_file_name) as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)
            for line in reader:
                csv_data[line[0]] = line[1:]
                author_stat[line[1]] += 1
    except Exception as e:
        print(e)

    return csv_data, author_stat


def csv_select(sorce_csv_data, target_authors):
    return { name: data for name, data in sorce_csv_data.items() if data[0] in target_authors }


def load_images(csv_data, location = "train_sample"):
    data = []
    labels = []

    for subdir, dirs, files in os.walk(location):
        for file in files:
            if file in csv_data:
                img_loc = os.path.join(subdir, file)
                img = image.load_img(img_loc, target_size=(256, 256))
                labels.append(csv_data[file][0])
                data.append(np.array(img))

                if len(labels) % 2000 == 0:
                    print(len(labels), "images loaded")

    # gc.collect() - nem volt sok értelme
    # byte-ként is lehetne tárolni: np.array(data, dtype="uint8") - ennek sem volt sok értelme
    return np.array(data), np.array(labels)


if __name__ == "__main__":
    print()

    csv_data = csv_load()
    images, labels = load_images(csv_data)
