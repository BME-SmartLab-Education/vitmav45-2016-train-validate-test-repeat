import csv
import os
import gc
import operator
import numpy as np
from collections import defaultdict
from keras.preprocessing import image

def csv_load(csv_file_name = "train_info_modified_fixed.csv"):
	"""	Load the labels for the adatset from a csv file, from the given path. """

    csv_data = {}
    # Store the number of occurences of each author. By default, it is 0.
    author_stat = defaultdict(int)

    with open(csv_file_name, encoding='utf8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        for line in reader:
        	# The first artribute is the filename, it will be the key. Other attributes are the values.
            csv_data[line[0]] = line[1:]
            # The second attribute is the author, so increase occurence number
            author_stat[line[1]] += 1

    # Return the stistics sorted as a list, because we want to use the most represented author's pictures.
    return csv_data, sorted(author_stat.items(), key=operator.itemgetter(1))

def csv_select(sorce_csv_data, author_stat):
	""" Filter the dataset description with the given authors. """

	# Let's assume that the author_stat object is from the csv_load function above. So we have a 
	# list of tuples. Then we have to get rid of occurance numbers.
    target_authors = [label for label, n in author_stat]
    return { name: data for name, data in sorce_csv_data.items() if data[0] in target_authors }

def load_images(csv_data, location = "train_sample"):
	""" Load the images which are in the csv_data from the given path, and return the list of images 
		and corresponding authors as labels. """

    data = []
    labels = []
    
    for subdir, dirs, files in os.walk(location):
        for file in files:
            if file in csv_data:
            	# Find and load image file with specified target size
                img_loc = os.path.join(subdir, file)
                img = image.load_img(img_loc, target_size=(256, 256))

                # Append data to lists
                data.append(np.array(img))
                labels.append(csv_data[file][0])

                if len(labels) % 2000 == 0:
                    print(len(labels), "images loaded")

    print(len(labels), "images in the result")
    return np.array(data), np.array(labels)

if __name__ == "__main__":
    print()
    csv_data, _ = csv_load()
    images, labels = load_images(csv_data)
