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


def csv_select(sorce_csv_data, author_stat):
    target_authors = [label for label, n in author_stat]
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

                if len(labels) % 2000 == 0:
                    print(len(labels), "images loaded")

    print(len(labels), "images in the result")
    return np.array(data), np.array(labels)


if __name__ == "__main__":
    print()
    csv_data, author_stat = csv_load()
    images, labels = load_images(csv_data)
