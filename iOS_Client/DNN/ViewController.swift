//
//  ViewController.swift
//  DNN
//
//  Created by Nagy Peter on 2016. 12. 06..
//  Copyright © 2016. train_validate_test_repeat. All rights reserved.
//

import UIKit
import Alamofire

extension NSMutableData {
    
    func appendString(string: String) {
        let data = string.data(using: String.Encoding.utf8, allowLossyConversion: true)
        append(data!)
    }
}


class ViewController: UIViewController , UIImagePickerControllerDelegate,UINavigationControllerDelegate{

    
    @IBOutlet weak var imageView: UIImageView!
    @IBOutlet weak var result: UITextView!
    
    @IBAction func upload(_ sender: Any) {
        if UIImagePickerController.isSourceTypeAvailable(UIImagePickerControllerSourceType.photoLibrary){
            let imagePicker = UIImagePickerController()
            imagePicker.delegate = self
            imagePicker.sourceType = UIImagePickerControllerSourceType.photoLibrary
            imagePicker.allowsEditing = true
            self.present(imagePicker,animated: true, completion: nil)
        }
    }
    
    func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [String : Any]) {
        if let pickedImage = info[UIImagePickerControllerOriginalImage] as? UIImage {
            self.imageView.image = pickedImage
            callService(image: pickedImage)
        }
        self.dismiss(animated: true, completion: nil);
    }
    
    func generateBoundary() -> String{
        return "Boundary-\(NSUUID().uuidString)"
    }
    
    func callService(image: UIImage){
        Alamofire.upload(multipartFormData: {
            multipartFormData in
            
                if let imageData = UIImageJPEGRepresentation(image, 1){
                    multipartFormData.append(imageData, withName: "file", fileName: "file.jpg", mimeType: "image/jpeg");
                }
            
        },to: "http://localhost:5000",encodingCompletion: {
            encodingResult in switch encodingResult {
            case .success(let upload, _, _):
                upload.responseJSON { response in
                    if let result = response.result.value {
                        let JSON = result as! [AnyObject]
                    
                        var str = "";
                        
                        for i in 0 ..< 3 {
                            let percentage = Double(round(1000000*Double(JSON[i][0] as! String)!)/1000000)
                            str +=  (String(format:"%.6f",percentage)) + " : Painter " + (JSON[i][1] as! String) + "\n"
                            
                        }
                        
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
        imageView.image = UIImage(named:"placeholder.png",in: Bundle(for:type(of:self)),compatibleWith:nil)
        // Do any additional setup after loading the view, typically from a nib.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


}

