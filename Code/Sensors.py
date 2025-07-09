import time
import board
import adafruit_scd4x
from adafruit_apds9960.apds9960 import APDS9960
from adafruit_apds9960 import colorutility
import logging

class Sensors:
    def __init__(self):
      try:
        logging.info("Initializing I2C")
        self.i2c = board.I2C()
        logging.info("Initializing Lux sensor")
        self.apds = APDS9960(self.i2c)
        self.apds.enable_color = True
        self.apds.color_gain = 0    #0=1x, 1=4x, 2=16x, 3 = 64x
        self.apds.color_integration_time = 72   # was 72, 37
        logging.info("Initializing CO2 sensor")
        self.scd4x = adafruit_scd4x.SCD4X(self.i2c)
        self.scd4x.start_periodic_measurement()
      except Exception as e:
          logging.error("Failed to initialize all sensors: " + str(e))

    def readSensors(self):
        while not self.scd4x.data_ready:
            time.sleep(1)
        self.CO2 = int(self.scd4x.CO2)
        self.tempC = int(self.scd4x.temperature)
        self.humd = int(self.scd4x.relative_humidity)
        
        while not self.apds.color_data_ready:
            time.sleep(0.005)
        self.red, self.green, self.blue, self.clear = self.apds.color_data
 #       self.colorTemp = int(colorutility.calculate_color_temperature(self.red, self.green, self.blue))
 #       self.lux = int(colorutility.calculate_lux(self.red, self.green, self.blue))
 #      conversion factor 0.443 based on comparison with TSL2591 Lux values
 #	lux returned as umol  
        self.lux = int((self.clear/1.475) * 0.443 * 0.0135)  # gain = 0 PPFD 
        self.colorTemp = -1
       

    def getAirStr(self):
        return str(self.CO2) + "," + str(int(self.tempC)) + "," + \
               str(int(self.humd))
    
    def getLuxStr(self):
        return str(self.lux) + "," + str(self.colorTemp) + "," + \
               str(self.red) + "," + str(self.green) + ","  + \
               str(self.blue) + "," + str(self.clear)
               




    
