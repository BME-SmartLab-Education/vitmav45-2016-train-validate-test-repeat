#Flask Web Service 
##Details: 
The web service uses our Deep Neural Network implementation to return the likelyhood of from a set of painters which one's style matches the style of the observed painting the most. 
The web service is based of Flask, a python framework, and uses its image upload script. What we contribute here, is that we transform the uploded image in order to be able to pass it to the network as input.
The service uses the model and weights exported from our trained Inception V3 network.

##Input
The server listens on port:<b>5000</b>, therefore can be reached at http://localhost:5000.
The service waits for multipart <b>image/jpeg</b> data, the name of the MultipartData package <b>must</b> be file.

###cURL

The service can be tested with the following cURL call:
```
curl -F "file=@./relative/path/to/image" http://localhost:5000 -X POST
```

##Output

The service returns with a valid JSON response in the following form:
```
[ 
  [ "likelihood - 0.xxxxxx", "Painter ID"],
  [...],
   ...
]
```
###One example response:
```
[
  ["0.583585", "9"],
  ["0.362166", "3"],
  ["0.0380105", "4"],
  ["0.015131", "0"],
  ...
]
```
###NOTE
The files model.json and sulyok.hdf5 (weights) are not included due to Github file size restrictions. In order to use the web service, please generate the files from the network.
</br>
Tutorial:</br>
http://machinelearningmastery.com/save-load-keras-deep-learning-models/
