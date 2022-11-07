from mfrc522 import MFRC522
from machine import I2C, Pin, SPI, PWM
from pico_i2c_lcd import I2cLcd
from time import sleep
import utime


###LCD Definition###########
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=100000)
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)
#lcd.putstr("LCD under reader does not work")
lcd.putstr("Scan Tag...")
############################

###Buzzer Definition########
buzzer = PWM(Pin(15))
############################

###RFID Definition###########
reader = MFRC522(spi_id=0,sck=2,miso=4,mosi=3,cs=1,rst=0)
############################


###Servo Definition#########
pwm = PWM(Pin(18))
pwm.freq(50)
############################


###LED Definition###########
masterLed=Pin(8,Pin.OUT)
redLed=Pin(9,Pin.OUT)
greenLed=Pin(10,Pin.OUT)


############################

print("Scan Tag...")
print("")
#lcd.putstr("ECE388\n")
#lcd.putstr("Scan Tag...")

tones = {
"B0": 31,
"C1": 33,
"CS1": 35,
"D1": 37,
"DS1": 39,
"E1": 41,
"F1": 44,
"FS1": 46,
"G1": 49,
"GS1": 52,
"A1": 55,
"AS1": 58,
"B1": 62,
"C2": 65,
"CS2": 69,
"D2": 73,
"DS2": 78,
"E2": 82,
"F2": 87,
"FS2": 93,
"G2": 98,
"GS2": 104,
"A2": 110,
"AS2": 117,
"B2": 123,
"C3": 131,
"CS3": 139,
"D3": 147,
"DS3": 156,
"E3": 165,
"F3": 175,
"FS3": 185,
"G3": 196,
"GS3": 208,
"A3": 220,
"AS3": 233,
"B3": 247,
"C4": 262,
"CS4": 277,
"D4": 294,
"DS4": 311,
"E4": 330,
"F4": 349,
"FS4": 370,
"G4": 392,
"GS4": 415,
"A4": 440,
"AS4": 466,
"B4": 494,
"C5": 523,
"CS5": 554,
"D5": 587,
"DS5": 622,
"E5": 659,
"F5": 698,
"FS5": 740,
"G5": 784,
"GS5": 831,
"A5": 880,
"AS5": 932,
"B5": 988,
"C6": 1047,
"CS6": 1109,
"D6": 1175,
"DS6": 1245,
"E6": 1319,
"F6": 1397,
"FS6": 1480,
"G6": 1568,
"GS6": 1661,
"A6": 1760,
"AS6": 1865,
"B6": 1976,
"C7": 2093,
"CS7": 2217,
"D7": 2349,
"DS7": 2489,
"E7": 2637,
"F7": 2794,
"FS7": 2960,
"G7": 3136,
"GS7": 3322,
"A7": 3520,
"AS7": 3729,
"B7": 3951,
"C8": 4186,
"CS8": 4435,
"D8": 4699,
"DS8": 4978
}


################################Buzzer Code Starts###################################
song = ["E5","G5","A5","P","E5","G5","B5","A5","P","E5","G5","A5","P","G5","E5"]

def playtone(frequency):
    buzzer.duty_u16(9999)
    buzzer.freq(frequency)

def bequiet():
    buzzer.duty_u16(0)

def playsong(mysong):
    for i in range(len(mysong)):
        if (mysong[i] == "P"):
            bequiet()
        else:
            playtone(tones[mysong[i]])
        sleep(0.3)
    bequiet()
#playsong(song)
################################Buzzer Code Ends###################################

while True:
    reader.init()
    (stat, tag_type) = reader.request(reader.REQIDL)
    if stat == reader.OK:
        (stat, uid) = reader.SelectTagSN()
        if stat == reader.OK:
            card = int.from_bytes(bytes(uid),"little",False)
            
            #Accepted Card
            if card == 2742357347:
                print("Card ID: "+ str(card)+" PASS")
                sleep(1)
                greenLed.on() #LED on
                ##Start Buzzer
                buzzer.freq(tones["C5"]) # set the frequency to match pitch C5
                buzzer.duty_u16(1000000000) # set the duty cycle for the pulses to be 1000/65535=1.5%
                
                ######Servo Code Starts#######
                #Lift Servo(open)
                pwm.duty_u16(9999)#rotate gate counter clockwise to open
                sleep(0.065)
                pwm.duty_u16(0)
                #Delay with servo open
                sleep(2) #delay for gate open
                #Close Servo
                pwm.duty_u16(500)#rotate gate clockwise
                sleep(0.065)
                pwm.duty_u16(0)
                sleep(2)
                ######Servo Code Ends#######
                
                
                buzzer.duty_u16(0)##Stop Buzzer
                #playsong(song)
                greenLed.off()

                
            #############Master Key##############################
            elif card == 216440211:
                
                print("Card ID: "+ str(card)+" PASS")
                masterLed.on()
                buzzer.freq(tones["C6"]) # set the frequency to match pitch C5
                buzzer.duty_u16(1000000000) # set the duty cycle for the pulses to be 1000/65535=1.5%
                   ######Servo Code Starts#######
                #Lift Servo(open)
                pwm.duty_u16(9999)#rotate gate counter clockwise to open
                sleep(0.065)
                pwm.duty_u16(0)
                #Delay with servo open
                sleep(2) #delay for gate open
                #Close Servo
                pwm.duty_u16(500)#rotate gate clockwise
                sleep(0.065)
                pwm.duty_u16(0)
                sleep(2)
                ######Servo Code Ends#######
                playsong(song)
                masterLed.off()
               
            
            ##################Any other card than defined######################   
            else:
                print("Card ID: "+ str(card)+" UNKNOWN CARD!")
                #Red Led On
                redLed.on()
                ####Buzzer Code for Access Denied#############
                buzzer.freq(tones["C5"]) # set the frequency to match pitch C5
                buzzer.duty_u16(999999) # set the duty cycle for the pulses to be 1000/65535=1.5%
                sleep(5)
                buzzer.duty_u16(0)
                #Red Led Off
                redLed.off()
                
   
   

                
