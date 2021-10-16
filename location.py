import logging                               
import requests
import json
import re

class Location:

    IP_LOCATION_URI = 'http://ipinfo.io/json'
    TIMEOUT = 5

    def __init__(self):
        self.lat = 0
        self.lng = 0

    def __getLocationFromIP(self):
        try:
            data = requests.get(self.IP_LOCATION_URI, timeout = self.TIMEOUT)
        except requests.exceptions.Timeout:
            logging.error('Timed out while doing get: ' + self.IP_LOCATION_URI)
        except Exception as e:
            logging.exception('Exception while doing get')
        
        if (data is None or data.status_code != requests.codes.ok):
            return

        json_data = json.loads(data.text)
        if 'loc' not in json_data:
            return

        logging.debug("{0}".format(json_data))

        res = list(map(float, re.findall(r'[-+]?\d*\.\d+|\d+', json_data['loc'])))
        self.lat = res[0]
        self.lng = res[1]

    def getLocation(self):
        self.__getLocationFromIP()

        return {'lat': self.lat, 'lng': self.lng}
