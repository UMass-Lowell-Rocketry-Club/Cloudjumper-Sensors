# Copyright 2026 UMass Lowell Rocketry

## This file contains the code for the radio
import sys
import sx126x # LoRa HAT
import tomllib # Read configuration file
import time
import threading

config = None
with open("config.toml", "rb") as f:
    config = tomllib.load(f)
assert(config is not None)

radio = None
is_vehicle = config["setup"]["is_vehicle"]
if is_vehicle:
    from gps import gps_rocketry

radio_address = config["setup"]["vehicle_address"] if is_vehicle else config["setup"]["ground_address"]
send_address = config["setup"]["vehicle_address"] if not is_vehicle else config["setup"]["ground_address"]
is_delaying = False
is_print_delaying = False
output_print_delay = config["setup"]["output_print_delay"] or 5 # Seconds

def delay(seconds: int):
    global is_delaying
    if is_delaying:
        return
    is_delaying = True
    time.sleep(seconds)
    is_delaying = False

def test_message_format():
    offset_frequence = int(915)-(850 if int(915)>850 else 410)
    radio = sx126x.sx126x(serial_num = config["setup"]["serial_port"],freq=config["setup"]["frequency"],addr=radio_address,power=config["setup"]["transmit_power"],rssi=True,air_speed=config["setup"]["air_speed"],relay=False)

    if is_vehicle:
        gps = gps_rocketry()

    while True:
        if is_vehicle:
            if not is_delaying:
                print("Sending...")
                threading.Thread(target=delay, kwargs={"seconds": output_print_delay}).start()
            
            gps.update_gps_data()
            msg = gps.dataMsg
            msg = msg.encode()
            start = "START".encode()
            end = "END\0\0\0\0\n".encode()
            data = start + msg + end
            radio.send(data)
            time.sleep(0.5)
        else:
            r_buff = radio.receive()
            print(str(r_buff))
            if not is_delaying:
                print("Receiving...")
                threading.Thread(target=delay, kwargs={"seconds": output_print_delay}).start()

if __name__ == '__main__':
    test_message_format()
