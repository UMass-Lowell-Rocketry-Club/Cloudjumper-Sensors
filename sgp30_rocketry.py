import time
import board
import busio
import tomllib
import adafruit_sgp30
from dataclasses import dataclass
### Capabilities of the SGP30 sensor include Ethanol, H2, TVOC, and eCO2

@dataclass
class SGP30:
    ethanol: int | None
    h2: int | None
    eco2:  int | None         
    tvoc: int | None     
    

class sgp30_sensor:
    def __init__(self):
        self.config = None
        with open("config.toml", "rb") as f:
            self.config = tomllib.load(f)
        assert(self.config is not None)
        temperature_celsius = self.config["setup"]["vehicle"]["sgp30_temperature_celsius"] or 15
        relative_humidity = self.config["setup"]["vehicle"]["sgp30_relative_humidity_percent"] or 50
        i2c = board.I2C()
        self.sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)
        print("SGP30: serial #", [hex(i) for i in self.sgp30.serial])

        print(f"SGP30: Using set temperature and humidity {temperature_celsius}C, {relative_humidity}%")
        self.sgp30.set_iaq_relative_humidity(celsius=temperature_celsius, relative_humidity=relative_humidity)

        print(f"SGP30: Baseline eC02 = 0x{self.sgp30.baseline_eCO2:x}, TVOC = 0x{self.sgp30.baseline_TVOC:x}")

    def check_attr(self, attr):
        try:
            val = getattr(self.sgp30, attr)
            return val if isinstance(val, int) else None
        except(AttributeError,RuntimeError):
            return None
    def get_measurements(self) -> SGP30:
        return SGP30(
            ethanol=self.check_attr("Ethanol"),
            h2= self.check_attr("H2"),
            eco2=self.check_attr("eCO2"),
            tvoc= self.check_attr("TVOC")
        )
        #msg = f"eCO2: {self.sgp30.eCO2} | TVOC: {self.sgp30.TVOC}"
        #return msg