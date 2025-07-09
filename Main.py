from UI import UI
from SettingsV2 import Settings		# using V2 json
from Sensors import Sensors
from LCD import LCD
from LightPanel import LightPanel
from Camera import Camera
from StoreData import StoreData
from MIOWS import MIOWS
from AWS import AWS
from time import sleep
import datetime  # Import the datetime module to work with dates and times
from datetime import time
import logging
import signal
import sys
import traceback

# setup ^C handler

def signal_handler(sig, frame):
    lp = LightPanel()
    lp.all_off()
    print ("\n\nExiting...")
    lcd.message("Exiting...")
    sleep(5)
    print("\nTurn off 5V power before shutdown")
    lcd.message("Turn off 5V pwr\nbefore shutdown")
    logging.info("Program exited via ^C")
    sys.exit(0)

# Main Program

sensor_delay = 5 * 60 # in seconds
camera_delay = 1 * 3600 # in seconds 3600 = 1 hour  
image_path = "/home/pi/ExoLabV1/images/"
using_AdafruitIO = False	# set True when using AdafruitIO services
using_MagnitudeIO = False	# set True when using MagnitudeIO services

recent_photo_name =""
recent_photo_url = ""

signal.signal(signal.SIGINT, signal_handler)

# set up logging

logging.basicConfig(filename='ExoLab.log', level=logging.INFO, 
   format="{asctime} - ExoLab - {levelname} - {message}", style ="{", datefmt="%Y-%m-%d %H:%M:%S")
logging.info("Starting ExoLab V1.2")
 
# startup program

try:
    lcd = LCD()
    lcd.message("Starting...")

    settings = Settings()
    settings.getSettings()
    lcd.message("Settings loaded")

    lp = LightPanel()
    camera = Camera(image_path,camera_delay,lp)
    s = Sensors()
    sd = StoreData()
    lcd = LCD()
    aws = AWS()
    miows = MIOWS()
    camera.setDeviceId(miows.getSerialNumber())
    aws.setDeviceSerialNumber(miows.getSerialNumber())


    lp.setTimeOn(LightPanel.LEFT_PANEL, settings.leftPanelTimeOn)
    lp.setTimeOff(LightPanel.LEFT_PANEL, settings.leftPanelTimeOff)
    lp.setup(LightPanel.LEFT_PANEL, settings.leftPanelColor, settings.leftPanelIntensity)

    lp.setTimeOn(LightPanel.RIGHT_PANEL, settings.rightPanelTimeOn)
    lp.setTimeOff(LightPanel.RIGHT_PANEL, settings.rightPanelTimeOff)
    lp.setup(LightPanel.RIGHT_PANEL, settings.rightPanelColor, settings.rightPanelIntensity)

    print ("Verifying lighting for 10 seconds")
    lcd.message("Verifying lights\nfor 10 seconds")

    lp.all_off()
    lp.all_on()
    sleep(10)
    lp.all_off()
    
    print ("Starting - Use ^C to exit program")
    lcd.message("Starting..\nUse ^C to exit")
    sleep(5)

except Exception as e:
    logging.error("Startup Exception: " + str(e))
    logging.error(traceback.format_exc())
    print(str(e))
    print(traceback.format_exc())

else:
    logging.info("Startup Complete - Entering Program Loop")
    catchallExceptionNumber = 1
    while True: # loop until ^C or multiple fatal errors
        try:
            timestamp = datetime.datetime.now()
            
            lightChange = lp.checkClock()
            if (lightChange):
                print("Lighting has changed")
                camera.triggerPhoto()	# take photo after every light change    
            fileName = camera.process() # take photo after light change or when camera_delay expires
            
            s.readSensors()
            print (timestamp.strftime("%x %X ") + (s.getAirStr()) + " " + (s.getLuxStr()) + "\n")
            lcd.displayData(int(s.tempC), int(s.humd), s.CO2, s.lux)
            sd.storeData(fileName, s, lp)  # always store data locally
            
            if (using_AdafruitIO):
                aio.sendData(s.tempC, s.humd, s.CO2, s.lux, lp.leftColor, lp.leftIntensity, lp.rightColor, lp.rightIntensity)
            
            if (using_MagnitudeIO):
                miows.postSensor(s.tempC, s.humd, s.CO2, s.lux)
            
                if (fileName != ""):
                    recent_photo_name = fileName
                    local_fileName = camera.pathName + fileName
                    url = aws.uploadToAWS(local_fileName, fileName)
                    if url != "":
                        print(url)
                        recent_photo_url = url
                if (recent_photo_name != "" and recent_photo_url != ""):
                    miows.postImage(recent_photo_name, recent_photo_url)
                    logging.info("Posted Image: " + recent_photo_url)
                
            sleep(sensor_delay)
            
            
        except Exception as e:
            logging.error("Catchall Exception # " + str(catchallExceptionNumber) + ": " + str(e))
            logging.error(traceback.format_exc())
            logging.info("Restarting...")
            print("Catchall Exception # " + str(catchallExceptionNumber) + ": " + str(e))
            print(traceback.format_exc())
            catchallExceptionNumber = catchallExceptionNumber + 1
            if (catchallExceptionNumber < 100):
                print("Restarting...")
                continue
            else:
                lp.all_off()
                print ("\n\nToo many exceptions - exiting")
                lcd.message("Too many exceptions\nExiting...")
                sleep(5)
                print("\nTurn off 5V power before shutdown")
                lcd.message("Turn off 5V pwr\nbefore shutdown")
                logging.error("Too many exceptions - Program exited.")
                sys.exit(1)
                

