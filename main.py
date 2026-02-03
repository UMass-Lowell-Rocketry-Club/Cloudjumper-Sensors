# Copyright 2026 UMass Lowell Rocketry

## This file contains the code for the radio
import sys
#import sx126x # LoRa HAT

config = {
    "frequency_mhz": 915, # FCC unlicensed between 902-928MHz
    "transmit_power_dbm": 22,
    "ground_station_address": 0, # Addresses MUST be different for ground station & rocket
    "vehicle_address": 65535,
    "air_speed": 2400 # Air speed (transmit speed) in bits per second. See sx126x.py for valid options
}

def init_radio():
    return
    #radio = sx126x.sx126x(serial_num = "/dev/ttyS0",freq=config["frequency_mhz"],addr=config["frequency_mhz"],power=config["transmit_power_dbm"],rssi=True,air_speed=2400,relay=False)
    #
    # the sending message format
    #
    #         receiving node              receiving node                   receiving node           own high 8bit           own low 8bit                 own 
    #         high 8bit address           low 8bit address                    frequency                address                 address                  frequency             message payload
   # data = bytes([int(config["address"])>>8]) + bytes([int(config["address"])&0xff]) + bytes([]) + bytes([65535>>8]) + bytes([65535&0xff]) + bytes([node.offset_freq]) + get_t[2].encode()

def test_message_format():
    get_rec = ""
    print("")
    print("input a string such as \033[1;32m0,868,Hello World\033[0m,it will send `Hello World` to lora node device of address 0 with 868M ")
    print("please input and press Enter key:",end='',flush=True)

    while True:
        rec = sys.stdin.read(1)
        if rec != None:
            if rec == '\x0a': break
            get_rec += rec
            sys.stdout.write(rec)
            sys.stdout.flush()

    get_t = get_rec.split(",")

    offset_frequence = int(get_t[1])-(850 if int(get_t[1])>850 else 410)
    #
    # the sending message format
    #
    #         receiving node              receiving node                   receiving node           own high 8bit           own low 8bit                 own 
    #         high 8bit address           low 8bit address                    frequency                address                 address                  frequency             message payload
    data = bytes([int(get_t[0])>>8]) + bytes([int(get_t[0])&0xff]) + bytes([offset_frequence]) + bytes([65535>>8]) + bytes([65535&0xff]) + bytes([offset_frequence]) + get_t[2].encode()
    print(data)




if __name__ == '__main__':
    version_info = sys.version_info
    if sys.version_info < (3, 12):
        raise Exception(f'Python version too low: expected 3.13, got {sys.version_info}')
    elif sys.version_info > (3, 12):
        # TODO: Use logging modules for this
        print(f'WARN: Python version {sys.version_info} too high')
    test_message_format()