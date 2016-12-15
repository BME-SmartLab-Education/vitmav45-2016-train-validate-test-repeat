#TRAIN_VALIDATE_TEST_REPEAT
###VITMAV45 2016 GROUP PROJECT

Our task was to train a convolutional neural network (CNN)  to recognize the style of selected painters, and later on to determine the origin of a painting received as input. As fort the second part of the semester using the received results, we decided to recreate the learnt painter styles in a way, that the network is able to produce style from noise defined by the obtained features of given paintings.

#Train 
##Dependencies 
###Libraries
* _Keras_
* _TensorFlow_
* _Numpy_
* _Sklearn_
* _Scipy_

##Included files
* _preprocess2.py_ - Processing the csv input, scaling and transforming the input images into tensors
* _learn.py_ - Train the neural network using the input data
* _train_info_modified_fix.csv_ - Data containing painter details
* _/train_sample_ - Image set for painters

##Usage
Parameters are modifiable from code only. 

###Run training
```
python learn.py
```

###Input 
* **csv_file_name** - defined in _preprocess2.py_ | _cs_load_ function argument | path to the csv containing meta data 
* **location** - defined in _preprocess2.py_ | _load_images_ function argument | path to the directory containing the training set images

###Output
The output is an array with the size equal to the input size, containing 10 floats for each element. These floats represent the probability that the painter on a given index is the creater of the painting.
####Sample output:
```
[ 
 [0.9, ... , 0.01],
 [ ... ],
 ...
 ...
 [ ... ],
 [0.07, ... , 0.2]
]
```
