import csv
import os

import numpy as np
from keras.preprocessing import image


# artist = []
# title = []
# style = []
# genre = []
# date = []


def csv_load():
    csv_data = []
    file_name = 'train_info_modified_fixed.csv'

    try:
        with open(file_name) as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)
            for line in reader:
                csv_data.append(line)
    except Exception as e:
        print(e)

    # for x in data:
    #     image_file_names.append(x[0])
    #     artist.append(x[1])
    #     title.append(x[2])
    #     style.append(x[3])
    #     genre.append(x[4])
    #     date.append(x[5])

    return [x[0] for x in csv_data], csv_data


def load_images(img_file_names, location = "train_sample"):
    imgs = []
    img_name_dict = {}
    ind = 0
    for subdir, dirs, files in os.walk(location):
        for file in files:
            if file in img_file_names:
                img_loc = os.path.join(subdir, file)
                img = image.load_img(img_loc, target_size=(256, 256))
                imgs.append([ind, img])
                img_name_dict[file] = ind
                ind += 1
    return img_name_dict, imgs


def data_preprocess(imgs, data, img_name_dict):
    # for x in img_name_dict:
    #     print(x, img_name_dict[x])
    # print()

    trn_images = imgs

    trn_data = []
    for x in data:
        if x[0] in img_name_dict:
            element = x[:]
            element.insert(0, img_name_dict[x[0]])
            trn_data.append(element)
    trn_data.sort()

    # for x in trn_images:
    #     print(x)
    # print()
    #
    # for x in trn_data:
    #     if x[1] in img_name_dict:
    #         print(x)
    # print()

    trn_images = [np.array(x[1]) for x in trn_images]
    trn_data = [x[1:] for x in trn_data]

    # for x in trn_images:
    #     print(x)
    # print()

    result = []
    for x in trn_data:
        if x[0] in img_name_dict:
            result.append(x)
    #        print(x)
    #print()

    return np.array(trn_images), result


if __name__ == "__main__":
    print()

    image_file_names, data = csv_load()
    image_name_dict, images = load_images(image_file_names)
    train_images, train_data = data_preprocess(images, data, image_name_dict)
