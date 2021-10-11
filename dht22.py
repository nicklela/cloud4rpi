# -*- coding: utf-8 -*-
import logging
import Adafruit_DHT 
import time

DHT_PIN = 4  
RETRY_COUNT=5
HUMIDITY_MAX = 100
TEMPERATURE_MAX = 100

class DHT22(object):

    def __init__(self, dht_pin = DHT_PIN):
        self.sensor = Adafruit_DHT.DHT22 
        self.pin = DHT_PIN

    def read(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)
        
        retry_count = 0
        while(humidity is None or temperature is None):

            retry_count += 1
            if(retry_count > RETRY_COUNT):
                humidity = 0
                temperature = 0
                logging.error("No response from DHT22")
                break

            time.sleep(1)
            logging.warn("Failed to read DHT22, retry in {0}/{1}".format(retry_count, RETRY_COUNT))
            humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)

        if humidity > HUMIDITY_MAX:
            logging.error("Humidity is invalid:{0}".format(humidity))
            humidity = HUMIDITY_MAX

        if temperature > TEMPERATURE_MAX:
            logging.error("Humidity is invalid:{0}".format(humidity))
            temperature = TEMPERATURE_MAX

        return humidity, temperature

    def read_temperature(self):
        humidity, temperature = self.read()
        return round(temperature, 2)

    def read_humidity(self):
        humidity, temperature = self.read()
        return round(humidity, 2)

