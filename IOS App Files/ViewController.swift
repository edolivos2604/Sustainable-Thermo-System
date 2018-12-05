//
//  ViewController.swift
//  Thermo-System
//
//  Created by Edwin Olivos on 11/3/18.
//  Copyright © 2018 Olivos. All rights reserved.
//

import UIKit
import FirebaseDatabase
import Firebase

class ViewController: UIViewController, UITextFieldDelegate {
    
    @IBOutlet weak var tempLabel: UILabel!
    @IBOutlet weak var humiLabel: UILabel!
    @IBOutlet weak var idealTempMinLabel: UILabel!
    @IBOutlet weak var idealTempMaxLabel: UILabel!
    @IBOutlet weak var remaDaysLabel: UILabel!
    @IBOutlet weak var errorLabel: UILabel!
    
    @IBOutlet weak var systemLabel: UILabel!
    @IBOutlet weak var controlLabel: UILabel!
    
    @IBOutlet weak var systemSwitch: UISwitch!
    @IBOutlet weak var lightSwitch: UISwitch!
    @IBOutlet weak var waterSwitch: UISwitch!
    @IBOutlet weak var fansSwitch: UISwitch!
    @IBOutlet weak var heatSwitch: UISwitch!
    
    // Firebase reference
    var ref: DatabaseReference?
    
    var databaseHandleTemp: DatabaseHandle?
    var databaseHandleHumi: DatabaseHandle?
    var databaseHandleIdealMinTemp: DatabaseHandle?
    var databaseHandleIdealMaxTemp: DatabaseHandle?
    var databaseHandleRemaDays: DatabaseHandle?
    var databaseHandleError: DatabaseHandle?
    var databaseHandleLight: DatabaseHandle?
    var databaseHandleWater: DatabaseHandle?
    var databaseHandleFans: DatabaseHandle?
    var databaseHandleHeat: DatabaseHandle?
    
    // Array variables
    var postDataTemp = [String]()
    var postDataHumi = [String]()
    var postDataIdealMinTemp = [String]()
    var postDataIdealMaxTemp = [String]()
    var postDataRemaDays = [String]()
    var postDataErrors = [String]()
    
    // Variables
    var minTempData: String!
    var maxTempData: String!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        
        let email = "XXXXXX@gmail.com"
        let password = "XXXXXXXX"
        Auth.auth().signIn(withEmail: email, password: password)
        
        //self.maxTemp.delegate = self
        //maxTemp.backgroundColor = UIColor.white
        //self.minTemp.delegate = self
        //minTemp.backgroundColor = UIColor.white
        
        // Set the firebase reference
        ref = Database.database().reference()
        
        // Retrieve info from firebase
        databaseHandleTemp = ref?.child("Data/2018/November/Temperature").observe(.childAdded, with:{(snapshot)in
            // Code execute when a child is added under "Data/2018/November/Temperature"
            // Try to convert the value of snapshot to string
            let temp = snapshot.value as? String
            if let actualTemp = temp{
                // Append the temp data to postData array
                self.postDataTemp.append(actualTemp)
                // Reload the textField
                self.tempLabel.text = "Temperature:  "+actualTemp+" deg C"
            }
        })
        databaseHandleHumi = ref?.child("Data/2018/November/Humidity").observe(.childAdded, with:{(snapshot)in
            // Code execute when a child is added under "Data/2018/November/Humidity"
            // Try to convert the value of snapshot to string
            let humi = snapshot.value as? String
            if let actualHumi = humi{
                // Append the temp data to postData array
                self.postDataHumi.append(actualHumi)
                // Reload the textField
                self.humiLabel.text = "Humidity:  "+actualHumi+" %"
            }
        })
        databaseHandleIdealMinTemp = ref?.child("Data/2018/November/MinTemperature").observe(.childAdded, with:{(snapshot)in
            // Code execute when a child is added under "Data/2018/November/MinTemperature"
            // Try to convert the value of snapshot to string
            let idealMinTemp = snapshot.value as? String
            if let actualIdealMinTemp = idealMinTemp{
                // Append the temp data to postData array
                //self.postDataIdealMinTemp.append(actualIdealMinTemp)
                self.idealTempMinLabel.text = actualIdealMinTemp
            }
        })
        databaseHandleIdealMaxTemp = ref?.child("Data/2018/November/MaxTemperature").observe(.childAdded, with:{(snapshot)in
            // Code execute when a child is added under "Data/2018/November/MaxTemperature"
            // Try to convert the value of snapshot to string
            let idealMaxTemp = snapshot.value as? String
            if let actualIdealMaxTemp = idealMaxTemp{
                // Append the temp data to postData array
                //self.postDataIdealMaxTemp.append(actualIdealMaxTemp)
                // Reload the textField
                self.idealTempMaxLabel.text = actualIdealMaxTemp
            }
        })
        databaseHandleRemaDays = ref?.child("Data/2018/November/RemaDays").observe(.childAdded, with:{(snapshot)in
            // Code execute when a child is added under "Data/2018/November/MaxTemperature"
            // Try to convert the value of snapshot to string
            let remaDays = snapshot.value as? String
            if let actualRemaDays = remaDays{
                // Append the temp data to postData array
                //self.postDataIdealMaxTemp.append(actualIdealMaxTemp)
                // Reload the textField
                self.remaDaysLabel.text = " Remaining days:  "+actualRemaDays
            }
        })
        databaseHandleError = ref?.child("Data/2018/November/Errors").observe(.childAdded, with:{(snapshot)in
            // Code execute when a child is added under "Data/2018/November/MaxTemperature"
            // Try to convert the value of snapshot to string
            let errorText = snapshot.value as? String
            if let actualError = errorText{
                // Append the temp data to postData array
                //self.postDataIdealMaxTemp.append(actualIdealMaxTemp)
                // Reload the textField
                self.errorLabel.text = actualError
            }
        })
        
        let tap = UITapGestureRecognizer(target: self, action: #selector(ViewController.tapFunction))
        
        systemLabel.isUserInteractionEnabled = true
        systemLabel.addGestureRecognizer(tap)
        
        controlLabel.isUserInteractionEnabled = true
        controlLabel.addGestureRecognizer(tap)
    }
    
    @IBAction func systemOnOff(_ sender: UISwitch) {
        if (sender.isOn == true){
            // Insert info to firebase
            ref?.child("Data/2018/November").child("SystemOn").setValue(true)

            self.lightOn(lightSwitch)
            self.lightSwitch?.isEnabled = false
            self.fansOn(fansSwitch)
            self.fansSwitch?.isEnabled = false
            self.waterOn(waterSwitch)
            self.waterSwitch?.isEnabled = false
            self.heatOn(heatSwitch)
            self.heatSwitch?.isEnabled = false
        }
        else {
            // Insert info to firebase
            ref?.child("Data/2018/November").child("SystemOn").setValue(false)
            
            self.lightSwitch?.isEnabled = true
            self.lightOn(lightSwitch)
            self.fansSwitch?.isEnabled = true
            self.fansOn(fansSwitch)
            self.waterSwitch?.isEnabled = true
            self.waterOn(waterSwitch)
            self.heatSwitch?.isEnabled = true
            self.heatOn(heatSwitch)
        }
    }
    
    @IBAction func lightOn(_ sender: UISwitch) {
        databaseHandleLight = ref?.child("Data/2018/November/Light").observe(.childAdded, with:{(snapshot)in
            // Code execute when a child is added under "Data/2018/November/MaxTemperature"
            // Try to convert the value of snapshot to string
            if let lightOn = snapshot.value{
                if lightOn as! Bool == true{
                    sender.isOn = true
                }
                else{
                    sender.isOn = false
                }
            }
        })
    }
    
    @IBAction func fansOn(_ sender: UISwitch) {
        databaseHandleFans = ref?.child("Data/2018/November/Fans").observe(.childAdded, with:{(snapshot)in
            // Code execute when a child is added under "Data/2018/November/MaxTemperature"
            // Try to convert the value of snapshot to string
            if let fansOn = snapshot.value{
                if fansOn as! Bool == true{
                    sender.isOn = true
                }
                else{
                    sender.isOn = false
                }
            }
        })
    }
    
    @IBAction func waterOn(_ sender: UISwitch) {
        databaseHandleWater = ref?.child("Data/2018/November/Water").observe(.childAdded, with:{(snapshot)in
            // Code execute when a child is added under "Data/2018/November/MaxTemperature"
            // Try to convert the value of snapshot to string
            if let waterOn = snapshot.value{
                if waterOn as! Bool == true{
                    sender.isOn = true
                }
                else{
                    sender.isOn = false
                }
            }
        })
    }
    
    @IBAction func heatOn(_ sender: UISwitch) {
        databaseHandleHeat = ref?.child("Data/2018/November/Heat").observe(.childAdded, with:{(snapshot)in
            // Code execute when a child is added under "Data/2018/November/MaxTemperature"
            // Try to convert the value of snapshot to string
            if let heatOn = snapshot.value{
                if heatOn as! Bool == true{
                    sender.isOn = true
                }
                else{
                    sender.isOn = false
                }
            }
        })
    }
    
    @objc func tapFunction(sender:UITapGestureRecognizer) {
        
        self.lightSwitch?.isEnabled = true
        self.lightOn(self.lightSwitch as UISwitch)
        self.lightSwitch?.isEnabled = false
        
        self.fansSwitch?.isEnabled = true
        self.fansOn(self.fansSwitch as UISwitch)
        self.fansSwitch?.isEnabled = false
        
        self.waterSwitch?.isEnabled = true
        self.waterOn(self.waterSwitch as UISwitch)
        self.waterSwitch?.isEnabled = false
        
        self.heatSwitch?.isEnabled = true
        self.heatOn(self.heatSwitch as UISwitch)
        self.heatSwitch?.isEnabled = false
    }
    
    // Function to insert info to firebase
    //@IBAction func updateData(_ sender: Any) {
        // Insert info to firebase
        //tempMaxResult = maxTemp.text!
        //ref?.child("Data/2018/November").child("AppMaxTemperature").setValue(tempMaxResult!)
        //tempMinResult = minTemp.text!
        //ref?.child("Data/2018/November").child("AppMinTemperature").setValue(tempMinResult!)
    //}
    
    // Hide Keyboard when touches outside keyboard
    override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent?) {
        self.view.endEditing(true)
    }
}

