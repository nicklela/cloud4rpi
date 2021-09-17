# -*- coding: utf-8 -*-

import Adafruit_DHT 

DHT_PIN = 4  

class DHT22(object):

    def __init__(self, dht_pin = DHT_PIN):
        self.sensor = Adafruit_DHT.DHT22 
        self.pin = DHT_PIN

    def read(self):
        return Adafruit_DHT.read_retry(self.sensor, self.pin)

    def read_temperature(self):
        humidity, temperature = self.read()
        return round(temperature, 2)

    def read_humidity(self):
        humidity, temperature = self.read()
        return round(humidity, 2)

