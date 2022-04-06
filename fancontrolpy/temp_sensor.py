from pathlib import Path


class TempSensor:
    def __init__(self, num):
        self.num = num

    @property
    def path_temp(self):
        return Path(f'/sys/class/hwmon/hwmon1/temp{self.num}_input')

    @property
    def temp(self):
        """Returns the temperature in °C"""
        return float(self.path_temp.read_text()) / 1000
