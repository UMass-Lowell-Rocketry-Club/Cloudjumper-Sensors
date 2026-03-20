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
radio_address = config["setup"]["vehicle_address"] if is_vehicle else config["setup"]["ground_address"]
send_address = config["setup"]["vehicle_address"] if not is_vehicle else config["setup"]["ground_address"]
is_delaying = False
output_print_delay = config["setup"]["output_print_delay"] or 5 # Seconds

def delay(seconds: int):
    if is_delaying:
        return
    is_delaying = True
    time.sleep(seconds)
    is_delaying = False

def test_message_format():
    get_rec = ""
    print("")
    print("input a string such as \033[1;32m0,868,Hello World\033[0m,it will send `Hello World` to lora node device of address 0 with 868M ")
    print("please input and press Enter key:",end='',flush=True)

    offset_frequence = int(915)-(850 if int(915)>850 else 410)
    radio = sx126x.sx126x(serial_num = config["setup"]["serial_port"],freq=config["setup"]["frequency"],addr=radio_address,power=config["setup"]["transmit_power"],rssi=True,air_speed=config["setup"]["air_speed"],relay=False)
    #
    # the sending message format
    #
    #         receiving node              receiving node                   receiving node           own high 8bit           own low 8bit                 own 
    #         high 8bit address           low 8bit address                    frequency                address                 address                  frequency             message payload
    msg = "HelloFromVehicle"
    msg = msg.encode()
    data = bytes([int(send_address)>>8]) + bytes([int(send_address)&0xff]) + bytes([offset_frequence]) + bytes([radio_address>>8]) + bytes([radio_address&0xff]) + bytes([offset_frequence]) + bytes(msg)

    while True:
        if is_vehicle:
            if not is_delaying:
                print("Sending...")
            radio.send(data)
            time.sleep(2)
            threading.Thread(target=delay, args=output_print_delay).start()
        else:
            radio.receive()
            if not is_delaying:
                print("Receiving...")
                continue
            threading.Thread(target=delay, args=output_print_delay).start()




if __name__ == '__main__':
    version_info = sys.version_info
    if sys.version_info < (3, 12):
        raise Exception(f'Python version too low: expected 3.13, got {sys.version_info}')
    elif sys.version_info > (3, 12):
        # TODO: Use logging modules for this
        print(f'WARN: Python version {sys.version_info} too high')
    test_message_format()
