# ECE388
GitHub repository for ECE388 project. Place all project files here.



## Project Description
RFID Automated boom barrier <br/>
### Specifications

###### Inputs <br/>
- Raspberry Pi Pico W(Wireless)
- MRFC522 RFID Reader
  - Detects Mifare 1K Classic Cards based on UID
    - UID ( Unique Identifier)

###### Outputs <br/>

- LCD 
  - Indicate either access granted or access denied.
- Buzzer
  - Access granted buzzer sound1
  - Access denied buzzer sound2
  - Master key buzzer sound for demo!
 - Servo
  - Rotate servo if access is granted
  - Do nothing if access is denied.
  
  ###### Next Steps <br/>
  Following can be achieved using IFTTT, guide can be found [here](https://www.tomshardware.com/how-to/connect-raspberry-pi-pico-w-to-twitter-via-ifttt).
  - If access granted
    - Send notification
  - If access denied
    - Send notification
    
  
