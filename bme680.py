import board # generic board interface
import adafruit_bme680
import time

i2c = board.I2C() # Communicate over board's default I2C bus
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=True)

bme680.sea_level_pressure = 1028.0
temperature_offset = -5 # Measure the value of the temperature sensor to calculate offset


while True:
    print("\nTemperature: %0.1f C" % (bme680.temperature + temperature_offset))
    print("Gas: %d ohm" % bme680.gas)
    print("Humidity: %0.1f %%" % bme680.relative_humidity)
    print("Pressure: %0.3f hPa" % bme680.pressure)
    print("Altitude = %0.2f meters" % bme680.altitude)

    time.sleep(1)