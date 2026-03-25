import time

import board
import busio

import adafruit_gps


class gps_rocketry:
    dataMsg: str = ""
    gps = None
    def __init__(self):
        # Create a serial connection for the GPS connection using default speed and
        # a slightly higher timeout (GPS modules typically update once a second).
        # These are the defaults you should use for the GPS FeatherWing.
        # Connect UART rx to GPS module TX, and UART tx to GPS module RX.
        #tx = board.TX  # Use board.GP4 or other UART TX on Raspberry Pi Pico boards.
        #rx = board.RX  # Use board.GP5 or other UART RX on Raspberry Pi Pico boards.
        #uart = busio.UART(tx, rx, baudrate=9600, timeout=10)

        # for a computer, use the pyserial library for uart access
        # import serial
        # uart = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=10)

        # If using I2C, we'll create an I2C interface to talk to using default pins
        i2c = board.I2C()  # uses board.SCL and board.SDA
        # i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

        # Create a GPS module instance.
        #gps = adafruit_gps.GPS(uart, debug=False)  # Use UART/pyserial
        self.gps = adafruit_gps.GPS_GtopI2C(i2c, debug=False)  # Use I2C interface

        # Initialize the GPS module by changing what data it sends and at what rate.
        # These are NMEA extensions for PMTK_314_SET_NMEA_OUTPUT and
        # PMTK_220_SET_NMEA_UPDATERATE but you can send anything from here to adjust
        # the GPS module behavior:
        #   https://cdn-shop.adafruit.com/datasheets/PMTK_A11.pdf

        # Turn on the basic GGA and RMC info (what you typically want)
        self.gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
        # Turn on the basic GGA and RMC info + VTG for speed in km/h
        # gps.send_command(b"PMTK314,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
        # Turn on just minimum info (RMC only, location):
        # gps.send_command(b'PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
        # Turn off everything:
        # gps.send_command(b'PMTK314,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
        # Turn on everything (not all of it is parsed!)
        # gps.send_command(b'PMTK314,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0')

        # Set update rate to once a second (1hz) which is what you typically want.
        self.gps.send_command(b"PMTK220,1000")
        # Or decrease to once every two seconds by doubling the millisecond value.
        # Be sure to also increase your UART timeout above!
        # gps.send_command(b'PMTK220,2000')
        # You can also speed up the rate, but don't go too fast or else you can lose
        # data during parsing.  This would be twice a second (2hz, 500ms delay):
        # gps.send_command(b'PMTK220,500')


    def update_gps_data(self):
        self.gps.update()
        # Every second print out current location details if there's a fix.
        current = time.monotonic()
        if not self.gps.has_fix:
            # Try again if we don't have a fix yet.
            self.dataMsg = "NoFix"
            print("Waiting for fix...")
            return
        self.dataMsg = ""
        # We have a fix! (gps.has_fix is true)
        # Print out details about the fix like location, date, etc.
        print("=" * 40)  # Print a separator line.
        print(
            "Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}".format(  # noqa: UP032
                self.gps.timestamp_utc.tm_mon,  # Grab parts of the time from the
                self.gps.timestamp_utc.tm_mday,  # struct_time object that holds
                self.gps.timestamp_utc.tm_year,  # the fix time.  Note you might
                self.gps.timestamp_utc.tm_hour,  # not get all data like year, day,
                self.gps.timestamp_utc.tm_min,  # month!
                self.gps.timestamp_utc.tm_sec,
            )
        )
        print(f"Latitude: {self.gps.latitude:.6f} degrees")
        self.dataMsg += f"Lat {self.gps.latitude:.6f}"
        print(f"Longitude: {self.gps.longitude:.6f} degrees")
        self.dataMsg += f"Long {self.gps.longitude:.6f}"
        print(f"Precise Latitude: {self.gps.latitude_degrees} degs, {self.gps.latitude_minutes:2.4f} mins")
        self.dataMsg += f"PreciseLat {self.gps.latitude_degrees:.6f}, {self.gps.latitude_minutes:2.4f}"
        print(f"Precise Longitude: {self.gps.longitude_degrees} degs, {self.gps.longitude_minutes:2.4f} mins")
        print(f"Fix quality: {self.gps.fix_quality}")
        # Some attributes beyond latitude, longitude and timestamp are optional
        # and might not be present.  Check if they're None before trying to use!
        if self.gps.satellites is not None:
            print(f"# satellites: {self.gps.satellites}")
        if self.gps.altitude_m is not None:
            print(f"Altitude: {self.gps.altitude_m} meters")
            self.dataMsg += f"Alt {self.gps.altitude_m}"
        if self.gps.speed_knots is not None:
            print(f"Speed: {self.gps.speed_knots} knots")
        if self.gps.speed_kmh is not None:
            print(f"Speed: {self.gps.speed_kmh} km/h")
        if self.gps.track_angle_deg is not None:
            print(f"Track angle: {self.gps.track_angle_deg} degrees")
        if self.gps.horizontal_dilution is not None:
            print(f"Horizontal dilution: {self.gps.horizontal_dilution}")
        if self.gps.height_geoid is not None:
            print(f"Height geoid: {self.gps.height_geoid} meters")