//
//  ViewController.swift
//  DNN
//
//  Created by Nagy Peter on 2016. 12. 06..
//  Copyright © 2016. train_validate_test_repeat. All rights reserved.
//

import UIKit
import Alamofire

//extension fron NSMutableData class. With it one can appen string to NSData type
extension NSMutableData {
    func appendString(string: String) {
        let data = string.data(using: String.Encoding.utf8, allowLossyConversion: true)
        append(data!)
    }
}


class ViewController: UIViewController , UIImagePickerControllerDelegate,UINavigationControllerDelegate{

    //References to UI elements
    @IBOutlet weak var imageView: UIImageView!
    @IBOutlet weak var result: UITextView!
    
    //Function to upload picture from the Photo Library
    @IBAction func upload(_ sender: Any) {
        if UIImagePickerController.isSourceTypeAvailable(UIImagePickerControllerSourceType.photoLibrary){
            let imagePicker = UIImagePickerController()
            imagePicker.delegate = self
            imagePicker.sourceType = UIImagePickerControllerSourceType.photoLibrary
            imagePicker.allowsEditing = true
            //present the Photo Lib View as Model Controller
            self.present(imagePicker,animated: true, completion: nil)
        }
    }
    
    //Handle the image-picking event
    func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [String : Any]) {
        if let pickedImage = info[UIImagePickerControllerOriginalImage] as? UIImage {
            self.imageView.image = pickedImage
            callService(image: pickedImage)
        }
        self.dismiss(animated: true, completion: nil);
    }
    //generates boundary for the http header
    func generateBoundary() -> String{
        return "Boundary-\(NSUUID().uuidString)"
    }
   
    func callService(image: UIImage){
        Alamofire.upload(multipartFormData: {
            multipartFormData in
                //Converting UIImage type to a raw JPEG representation         
                if let imageData = UIImageJPEGRepresentation(image, 1){
                    //appending imageData to the multipart container
                    multipartFormData.append(imageData, withName: "file", fileName: "file.jpg", mimeType: "image/jpeg");
                }
            //sending the data to the webservice
        },to: "http://localhost:5000",encodingCompletion: {
            encodingResult in switch encodingResult {
            case .success(let upload, _, _):
                upload.responseJSON { response in
                    if let result = response.result.value {
                        let JSON = result as! [AnyObject]
                        //getting the response from the webservice
                        var str = "";
                        
                        for i in 0 ..< 3 {
                            let percentage = Double(round(1000000*Double(JSON[i][0] as! String)!)/1000000)
                            str +=  (String(format:"%.6f",percentage)) + " : Painter " + (JSON[i][1] as! String) + "\n"
                            
                        }
                        //updating UI
                        DispatchQueue.main.async() { () -> Void in
                            self.result.text = str as String!
                        }
                    }
                }
            case .failure(let encodingError):
                print(encodingError)
            }
        })
    }
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        imageView.contentMode = .scaleAspectFit
        //Placeholder image
        imageView.image = UIImage(named:"placeholder.png",in: Bundle(for:type(of:self)),compatibleWith:nil)
        // Do any additional setup after loading the view, typically from a nib.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


}

