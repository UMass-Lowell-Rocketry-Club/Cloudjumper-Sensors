import time
import board
import busio
import tomllib
import adafruit_sgp30

class sgp30_rocketry:
    def __init__(self):
        config = None
        with open("config.toml", "rb") as f:
            self.config = tomllib.load(f)
        assert(self.config is not None)
        temperature_celsius = config["setup"]["vehicle"]["sgp30_temperature_celsius"] or 15
        relative_humidity = config["sensors"]["sgp30"]["sgp30_relative_humidity_percent"] or 50
        i2c = board.I2C()
        self.sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)
        print("SGP30: serial #", [hex(i) for i in self.sgp30.serial])

        print(f"SGP30: Using set temperature and humidity {temperature_celsius}C, {relative_humidity}%")
        self.sgp30.set_iaq_relative_humidity(celsius=temperature_celsius, relative_humidity=relative_humidity)

        print(f"SGP30: Baseline eC02 = 0x{self.sgp30.baseline_eCO2:x}, TVOC = 0x{self.sgp30.baseline_TVOC:x}")

    def get_measurements(self) -> str:
        msg = f"eCO2: {self.sgp30.eCO2()} | TVOC: {self.sgp30.TVOC()}"
        return msg