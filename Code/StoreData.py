import datetime
import os.path

class StoreData:
        
    def storeData(self, imageFileName, sensor, lp):
        timestamp = datetime.datetime.now()
        line = timestamp.strftime("%x %X") + ","
        line = line + imageFileName +","
        line = line + sensor.getAirStr() + ","
        line = line + sensor.getLuxStr() + ","
        line = line + lp.getSettingsStr() + "\n"
        
        file = open(self.fileName, "a")
        file.write(line)
        file.close()
        
    def createFile(self):
        if (os.path.exists(self.fileName)):
            return
        else:
            heading = "timestamp,imageFile,CO2,tempC,humd,lux,colorTemp,red,green,blue,white,"
            heading = heading + "leftOn,leftOff,leftColor,leftBrightness,"
            heading = heading + "rightOn,rightOff,rightColor,rightBrightness \n"
            file = open(self.fileName, "a")
            file.write(heading)
            file.close()
            
    def __init__(self):
        self.success = True
        self.fileName = "/home/pi/ExoLabV1/ExoLab_Data.csv"
        self.createFile()