# -*- coding: utf-8 -*-

from time import sleep
import sys
import argparse
import logging
import os
import cloud4rpi
import rpi
from config import Configuration
from location import Location
from dht22 import DHT22

         
POLL_INTERVAL = 0.5  # 500 ms
LOG_FORMAT = '%(asctime)s %(levelname)s: %(message)s'
def debug_enabled(debug_enable: False):
    if(debug_enable is True):
        logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
    else:
        logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

def main():
    """
    parse user input
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="specify the config.json in other place", default=Configuration.DEFAULT_CONFIG)
    args = parser.parse_args()

    logging.info(os.path.basename(__file__) + ' start')

    """
    Get config
    """
    config = Configuration(args.config)
    try:
        config.load()
    except Exception as e:
        logging.error('Fail to load configuration from ' + config.file + ' due to {0}'.format(e))
        raise RuntimeError('Fail to load configuration') from e

    logging.debug('config {0}'.format(config.settings))

    """
    Initial devices
    """
    dht_sensor = DHT22()
    location = Location()


    """
    Put variable declarations here
    Available types: 'bool', 'numeric', 'string', 'location'
    """
    variables = {
        'Room Temp': {
            'type': 'numeric',
            'bind': dht_sensor.read_temperature
        },
         'Room Humidity': {
             'type': 'numeric',
             'bind': dht_sensor.read_humidity
         },
        'CPU Temp': {
            'type': 'numeric',
            'bind': rpi.cpu_temp
        },
        'Location': {
            'type': 'location',
            'bind': location.getLocation
        }
    }

    diagnostics = {
        'CPU Temp': rpi.cpu_temp,
        'IP Address': rpi.ip_address,
        'Host': rpi.host_name,
        'Operating System': rpi.os_name,
        'Client Version:': cloud4rpi.__version__,
    }
    device = cloud4rpi.connect(config.token)


    try:
        device.declare(variables)
        device.declare_diag(diagnostics)

        device.publish_config()

        # Adds a 1 second delay to ensure device variables are created
        sleep(1)

        data_timer = 0
        diag_timer = 0

        while True:
            if data_timer <= 0:
                device.publish_data()
                data_timer = config.interval

            if diag_timer <= 0:
                device.publish_diag()
                diag_timer = config.interval * 2

            sleep(POLL_INTERVAL)
            diag_timer -= POLL_INTERVAL
            data_timer -= POLL_INTERVAL

    except KeyboardInterrupt:
        cloud4rpi.log.info('Keyboard interrupt received. Stopping...')

    except Exception as e:
        error = cloud4rpi.get_error_message(e)
        cloud4rpi.log.exception("ERROR! %s %s", error, sys.exc_info()[0])

    finally:
        sys.exit(0)


if __name__ == '__main__':
    debug_enabled(False)
    main()
