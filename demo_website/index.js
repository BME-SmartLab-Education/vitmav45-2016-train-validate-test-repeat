var ndarray = require("ndarray")
var ops = require("ndarray-ops")
$(document).ready(function () {

    const model = new KerasJS.Model({
        filepaths: {
            model: "./keras/model.json",
            weights: "./keras/weights.buf",
            metadata: "./keras/metadata.json"
        },
        gpu: true
    });


    Dropzone.options.dropzone = {
        paramName: "file",
        maxFilesize: 15,
        uploadMultiple: false,
        parallelUploads: 1,
        maxFiles: 1,
        dictDefaultMessage: "Drop your image here!",
        accept: function (file, done) {
            $('#dropzone').hide();
            $('.imagepicker ul').fadeIn(500);
        },
        init: function () {
            this.on("addedfile", function (file) {
                if (this.files[1] != null) {
                    this.removeFile(this.files[0]);
                }
                var reader = new FileReader();
                reader.addEventListener("load", function (event) {
                    var img = new Image();
                    var copy = new Image();
                    img.src = event.target.result;
                    copy.src = event.target.result;
                    var W = 256
                    var H = 256
                  
                    var ctx = document.getElementById('input-canvas').getContext('2d')
                    ctx.drawImage(img, 0, 0, W, H);
                    const imageData = ctx.getImageData(0, 0, W, H)
                    const { data, width, height } = imageData
                    console.log(width)
                    console.log(height)
                    var data2 = ndarray(new Float32Array(data), [width, height, 4])
                    console.log(data2)
                    //for (var x = 0; x < W; ++x){
                    //  for (var y = 0; y < H; ++y){
                    //    data2[x][y] = data2[x][y].slice(0,3)
                    //  }
                    //}
                    var data3 = ndarray(new(Float32Array(width)))
                    console.log(data2.dimension)

                    var i = nj.images.read(img);
                    var resized = nj.images.resize(i, W, H)
                    console.log(resized);
                    
                    model.ready()
                        .then(() => {
                            const inputData = {
                                'input_1': new Float32Array(img)
                            }
                            console.log(inputData);

                            model.predict(inputData)
                                .then(outputData => {
                                    console.log(outputData);
                                }).catch(err => {
                                    console.log("Problem with predict");
                                })
                        }).catch(err => {
                            console.log("Problem with model ready");
                        })

                });
                reader.readAsDataURL(file);
            });
        }

    };
});