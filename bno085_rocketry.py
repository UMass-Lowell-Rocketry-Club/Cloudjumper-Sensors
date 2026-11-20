import time
import board
import busio
import tomllib
from adafruit_bno08x.i2c import BNO08X_I2C
from adafruit_bno08x import BNO_REPORT_ACCELEROMETER, BNO_REPORT_GYROSCOPE, BNO_REPORT_MAGNETOMETER, BNO_REPORT_MAGNETOMETER, BNO_REPORT_ROTATION_VECTOR
from micropython import const

class bno085_sensor:
    def __init__(self):
        self.config = None
        with open("config.toml", "rb") as f:
            self.config = tomllib.load(f)
        assert(self.config is not None)
        REPORT_INTERVAL = const(self.config["setup"]["vehicle"]["bno085_report_interval"]) or 100_000 # 100 Hz
        i2c = board.I2C()
        bno = BNO08X_I2C(i2c)
        bno.enable_feature(BNO_REPORT_ACCELEROMETER, REPORT_INTERVAL)
        bno.enable_feature(BNO_REPORT_GYROSCOPE, REPORT_INTERVAL)
        bno.enable_feature(BNO_REPORT_MAGNETOMETER, REPORT_INTERVAL)
        bno.enable_feature(BNO_REPORT_ROTATION_VECTOR, REPORT_INTERVAL)
        self.bno085 = bno
        print("BNO085: initialized")

    def get_measurements(self) -> str:
        accel_x, accel_y, accel_z = self.bno085.acceleration
        gyro_x, gyro_y, gyro_z = self.bno085.gyro
        mag_x, mag_y, mag_z = self.bno085.magnetic
        quat_i, quat_j, quat_k, quat_real = self.bno085.quaternion
        msg = (
            f"accel_x={accel_x:.6f} accel_y={accel_y:.6f} accel_z={accel_z:.6f} "
            f"gyro_x={gyro_x:.6f} gyro_y={gyro_y:.6f} gyro_z={gyro_z:.6f} "
            f"mag_x={mag_x:.6f} mag_y={mag_y:.6f} mag_z={mag_z:.6f} "
            f"quat_i={quat_i:.6f} quat_j={quat_j:.6f} quat_k={quat_k:.6f} quat_real={quat_real:.6f}"
        )
        return msg
