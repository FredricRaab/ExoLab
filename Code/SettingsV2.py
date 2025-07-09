from LightPanel import LightPanel
from MIOWS import MIOWS
import datetime  # Import the datetime module to work with dates and times
from datetime import date, time, datetime, timedelta
import json
import logging

class Settings:
    
    def __init__(self):
        self.defaultFile = "/home/pi/ExoLabV1/DefaultSettingsV2.json"
        # set defaults
        self.leftPanelColor = LightPanel.WHITE
        self.leftPanelIntensity = 10
        self.leftPanelTimeOn = time.fromisoformat("06:00")
        self.leftPanelTimeOff = time.fromisoformat("17:00")
        
        self.rightPanelColor = LightPanel.WHITE
        self.rightPanelIntensity = 10
        self.rightPanelTimeOn = time.fromisoformat("06:00")
        self.rightPanelTimeOff = time.fromisoformat("17:00")
        
    def	dumpSettings(self):
        print("Left Panel:")
        print(self.leftPanelColor)
        print(self.leftPanelIntensity)
        print(self.leftPanelTimeOn)
        print(self.leftPanelTimeOff)
        print("Right Panel:")
        print(self.rightPanelColor)
        print(self.rightPanelIntensity)
        print(self.rightPanelTimeOn)
        print(self.rightPanelTimeOff)
 
    def get_color(self, colorStr):
        if (colorStr == "red"):
            color = LightPanel.RED
        elif (colorStr == "green"):
            color = LightPanel.GREEN
        elif (colorStr == "blue"):
            color = LightPanel.BLUE
        elif (colorStr == "magenta"):
            color = LightPanel.MAGENTA
        else:
            color = LightPanel.WHITE
        return color
    
    def get_time_off(self, timeOn, hoursStr):
        hr = int(hoursStr)
        result = datetime.combine(date.today(),timeOn) + timedelta(hours=hr)
        return (result.time())
 
 
    def read_file(self):
        f = open(self.defaultFile, "r")
        settings = f.read()
        print (settings)
        return settings
    
    def parse_settings(self, jsonStr):
        data = json.loads(jsonStr)
        if data["result"]["mode"] == "dual":
            self.leftPanelColor = self.get_color(data["result"]["leftSettings"]["color"])
            self.leftPanelIntensity = int(data["result"]["leftSettings"]["intensity"])
            period = (data["result"]["leftSettings"]["photoperiod"])
            self.leftPanelTimeOff = self.get_time_off(self.leftPanelTimeOn, period)
  
            self.rightPanelColor = self.get_color(data["result"]["rightSettings"]["color"])
            self.rightPanelIntensity = int(data["result"]["rightSettings"]["intensity"])
            period = (data["result"]["rightSettings"]["photoperiod"])
            self.rightPanelTimeOff = self.get_time_off(self.rightPanelTimeOn, period)
        else:
            self.leftPanelColor = self.get_color(data["result"]["settings"]["color"])
            self.leftPanelIntensity = int(data["result"]["settings"]["intensity"])
            period = (data["result"]["settings"]["photoperiod"])
            self.leftPanelTimeOff = self.get_time_off(self.leftPanelTimeOn, period)
  
            self.rightPanelColor = self.get_color(data["result"]["settings"]["color"])
            self.rightPanelIntensity = int(data["result"]["settings"]["intensity"])
            period = (data["result"]["settings"]["photoperiod"])
            self.rightPanelTimeOff = self.get_time_off(self.rightPanelTimeOn, period)
        return

    def getSettings(self):
        miows = MIOWS()
        logging.info("Attempting to get settings from Server")
        jsonStr = str(miows.getConfig())
        try:
            data = json.loads(jsonStr)
            if data["type"] == "SUCCESS":
                self.parse_settings(jsonStr)
            else:
                jsonStr = None
        except Exception as e:
            logging.error("Exception parseing Server json: " + str(e))
            jsonStr = None
            
#        jsonStr = None    # comment for testing
        if (jsonStr == None):
            logging.info("Attempting to get settings from " + self.defaultFile)
            jsonStr = self.read_file()
        
        if (jsonStr != None):
            self.parse_settings(jsonStr)
            return
        else:
            logging.info("Using program defaults")
        
        
        
