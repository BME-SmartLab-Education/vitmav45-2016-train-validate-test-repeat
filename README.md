#TRAIN_VALIDATE_TEST_REPEAT
###VITMAV45 2016 GROUP PROJECT

Our task was to train a convolutional neural network (CNN)  to recognize the style of selected painters, and later on to determine the origin of a painting received as input. As fort the second part of the semester using the received results, we decided to recreate the learnt painter styles in a way, that the network is able to produce style from noise defined by the obtained features of given paintings.

#Train 
##Dependencies 
###Libraries
* Keras
* TensorFlow
* Numpy
* Sklearn
* Scipy

##Included files
* preprocess2.py - Processing the csv input, scaling and transforming the input images into tensors
* learn.py - Train the neural network using the input data
* train_info_modified_fix.csv - Data containing painter details
* /train_sample - Image set for painters

##Usage
Parameters are modifiable from code only. 

###Run training
```
python learn.py
```

###Input 
* csv_file_name - defined in preprocess2.py | cs_load function argument | path to the csv containing meta data 
* location - defined in preprocess2.py | load_images function argument | path to the directory containing the training set images

###Output
The output is an array with the size equal to the input size, containing 10 floats for each element. These floats represent the probability that the painter on a given index is the creater of the painting.
####Sample output:
```
[ 
 [0.9, ... , 0.01],
 [ ... ],
 ...
 ...
 [ ... ]
]
```
