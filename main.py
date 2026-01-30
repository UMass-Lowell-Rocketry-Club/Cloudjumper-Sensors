# Copyright 2026 UMass Lowell Rocketry

## This file contains the code for the radio
import sys
import sx126x # LoRa HAT

config = {
    "frequency_mhz": 902, # FCC unlicensed between 902-928MHz
    "transmit_power_dbm": 22,
    "address": 0, # Addresses might have to be same for both transmitter and receiver
    "air_speed": 2400 # Air speed (transmit speed) in bits per second. See sx126x.py for valid options
}

def init_radio():
    radio = sx126x.sx126x(serial_num = "/dev/ttyS0",freq=config["frequency_mhz"],addr=config["frequency_mhz"],power=config["transmit_power_dbm"],rssi=True,air_speed=2400,relay=False)
    payload = bytes('')

if __name__ == '__main__':
    version_info = sys.version_info
    if sys.version_info < (3, 12):
        raise Exception(f'Python version too low: expected 3.13, got {sys.version_info}')
    elif sys.version_info > (3, 12):
        # TODO: Use logging modules for this
        warn(f'WARN: Python version {sys.version_info} too high')
    init_radio()