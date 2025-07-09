import requests
import base64
from datetime import datetime
import logging


class MIOWS:
    
    def __init__(self):
        
        # verify these have not changed
        self.baseURL = 'https://streams.magnitude.io'
        self.confURL = 'https://magni.magnitude.io'
        
        #replace these with Magnitude.io provided serial number and password
        self.serialNumber = "xxxxxxxx" # replace 
        self.password = "xxxxxxxxx"  # replace
    
    def setSerialNumber(self, sn):
        self.serialNumber = sn
        
    def getSerialNumber(self):
        return self.serialNumber
        
    def setPassword(self, pw):
        self.password = pw
        
    def setBaseURL(self, url):
        self.baseURL = url
        
    def postSensor(self, temp, hum, co2, lux):
        UTCtime_str = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        auth_header = "Basic " + base64.b64encode(f"{self.serialNumber}:{self.password}".encode()).decode()
        header = {"Authorization": auth_header }

        sensor_data = {
            "type": "sensor",
            "time": UTCtime_str,
            "data": {
                "Time": UTCtime_str,
                "Temp": temp,
                "Hum": hum,
                "CO2": co2,
                "lux": lux
                }
            }
        
        try:
            response = requests.post(f"{self.baseURL}/devices/{self.serialNumber}/events", headers=header, json=sensor_data)
            print("Post Sensor Data response code: " + str(response.status_code))
            if (response.status_code != 200):
                logging.warning("Post Sensor Data response code: " + str(response.status_code)) 
            return(response.status_code)
        except requests.exceptions.RequestException as e:
            logging.error("Post Sensor Data Exception: " + str(e))
        return(0)
    
    def postImage(self, imageName, imageURL):
        UTCtime_str = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        auth_header = "Basic " + base64.b64encode(f"{self.serialNumber}:{self.password}".encode()).decode()
        header = {"Authorization": auth_header }

        image_data = {
            "type": "image",
            "time": UTCtime_str,
            "data": {
                "timestamp": UTCtime_str,
                "filename": imageName,
                "image": imageURL,
                }
            }
        
        try:
            response = requests.post(f"{self.baseURL}/devices/{self.serialNumber}/events", headers=header, json=image_data)
            print("Post ImageURL response code: " + str(response.status_code))
            if (response.status_code !=200):
                logging.warning("Post ImageURL response code: " + str(response.status_code))
            return(response.status_code)
        except requests.exceptions.RequestException as e:
            logging.error("Post ImageURL Exception: "+ str(e))
        return(0)
    
    def getLast2Events(self):
        auth_header = "Basic " + base64.b64encode(f"{self.serialNumber}:{self.password}".encode()).decode()
        header = {"Authorization": auth_header }

        print ("Get Last 2 Events")
        try:
            response = requests.get(f"{self.baseURL}/devices/{self.serialNumber}/events?sortDirection=desc&limit=2", headers=header)
            code = response.status_code
            print(code)
            if code == 200:
                print(response.json())
                return code
        except requests.exceptions.RequestException as e:
            print ("Unexpected Exception: " + str(e))
        return(0)
            
    def getConfig(self):
        auth_header = "Basic " + base64.b64encode(f"{self.serialNumber}:{self.password}".encode()).decode()
        header = {"Authorization": auth_header }

        print ("MIOWS.getConfig")
        try:
            response = requests.get(f"{self.confURL}/api/experiments/config/", headers=header)
            code = response.status_code
            print(code)
            if code == 200:
                data = str(response.json())
                print(response.json())
                data2 = data.replace("'", '"')
                print(data2)
                logging.info("MIOWS.getConfig successfull")
                return data2
        except requests.exceptions.RequestException as e:
            logging.error("MIOWS.getConfig Exception: " + str(e))
        return(None)

