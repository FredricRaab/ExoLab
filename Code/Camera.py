import datetime  # Import the datetime module to work with dates and times
from datetime import time
from time import sleep
import libcamera
from libcamera import controls
from picamera2 import Picamera2, Preview
from LightPanel import LightPanel
import logging


class Camera:
    def __init__(self, path_name, camera_delay, light_panel):
        self.pathName = path_name
        self.cameraDelay = camera_delay
        self.lp = light_panel
        self.lastPhoto = None
        self.deviceId = "Image"
        self.picam = Picamera2()
        self.picam.options["quality"] = 50
        config = self.picam.create_preview_configuration(main={"size": (1920, 1080)})
#         config["transform"] = libcamera.Transform(vflip=1) # flip image if cable is feeding upwards
        self.picam.configure(config)
#        self.picam.set_controls({"AfMode": 0, "LensPosition" : 30}) # not need for fisheye camera
 
    def setDeviceId(self, id):
        self.deviceId = id
        
    def triggerPhoto(self):
        self.lastPhoto = None  # force camera to take a picture
        
    def process(self):
        if self.lastPhoto is None:  #take photo upon startup
            fileName = self.take_photo()
            return fileName
        else:
            now = datetime.datetime.now()
            timeSince = (now - self.lastPhoto).total_seconds()
            if (timeSince < self.cameraDelay):
                return ""
            else: 
                fileName = self.take_photo()
                return fileName
    
    def take_photo(self):
        self.lp.all_white()  # turn all lights on full for photo
        self.lastPhoto = datetime.datetime.now()
        fileName = self.deviceId + "_" + self.lastPhoto.strftime("%y%m%d%H%M%S" + \
                   ".jpg")
        self.picam.start()
        sleep(2)
        self.picam.capture_file(self.pathName + fileName)
        logging.info("Photo taken: "+ fileName)
        print("Photo taken: "+ fileName)
        self.lp.restore_state()  #  restore lights to previous state
        sleep(3)  # wait for LEDs to dim to previous state
        return fileName
    
    