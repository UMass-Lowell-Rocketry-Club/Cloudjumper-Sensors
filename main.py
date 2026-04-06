# Copyright 2026 UMass Lowell Rocketry

## This file contains the code for the radio
import sx126x # LoRa HAT
import tomllib # Read configuration file
import time
import threading
import csv
from queue import Queue 

start_time=time.time()
config = None
with open("config.toml", "rb") as f:
    config = tomllib.load(f)
assert(config is not None)

radio = None
is_vehicle = config["setup"]["is_vehicle"]
if is_vehicle:
    from gps import gps_rocketry
    from sgp30_rocketry import sgp30_sensor

radio_address = config["setup"]["vehicle_address"] if is_vehicle else config["setup"]["ground_address"]
send_address = config["setup"]["vehicle_address"] if not is_vehicle else config["setup"]["ground_address"]
is_delaying = False
is_print_delaying = False
output_print_delay = config["setup"]["output_print_delay"] or 5 # Seconds
log_filename="gps_log.csv"
log_queue = Queue()

def csv_logger(filename, queue):
    with open(filename, "a", newline="") as f:
        writer=csv.writer(f)
        while True:
            data = queue.get()
            if data == "STOP":
                break
            writer.writerow(data)
            f.flush()
            queue.task_done()
    

threading.Thread(target=csv_logger, args=(log_filename, log_queue),daemon=True).start()

def delay(seconds: int):
    global is_delaying
    if is_delaying:
        return
    is_delaying = True
    time.sleep(seconds)
    is_delaying = False

def test_message_format():
    radio = sx126x.sx126x(serial_num = config["setup"]["serial_port"],freq=config["setup"]["frequency"],addr=radio_address,power=config["setup"]["transmit_power"],rssi=True,air_speed=config["setup"]["air_speed"],relay=False)

    if is_vehicle:
        gps = gps_rocketry()
        sgp30 = sgp30_sensor()

    while True:
        if is_vehicle:
            if not is_delaying:
                print("Sending...")
                threading.Thread(target=delay, kwargs={"seconds": output_print_delay}).start()
            
            gps.update_gps_data()
            gps_msg = gps.dataMsg
            sgp30_msg = sgp30.get_measurements()
            start_msg = "START"
            timestamp = round(time.time()-start_time,5) #calculates when this was received from when code was started up
            end_msg = "END"
            data_msg = start_msg + str(timestamp) + gps_msg + "\nSGP30: " + sgp30_msg + end_msg
            log_queue.put([time.time(), data_msg])

            data_utf8_bytes = data_msg.encode()

            radio.send(data_utf8_bytes)
            time.sleep(0.1)
        else:
            r_buff = radio.receive()
            received_msg = r_buff and str(r_buff) or None
            if received_msg:
                log_queue.put([time.time(), received_msg])
                print(received_msg)
            if not is_delaying:
                print("Receiving..." and ("no buff" if not r_buff else ""))
                threading.Thread(target=delay, kwargs={"seconds": output_print_delay}).start()

if __name__ == '__main__':
    test_message_format()
