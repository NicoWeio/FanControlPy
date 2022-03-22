from pathlib import Path
# import subprocess


class Fan:
    def __init__(self, num):
        self.num = num

    @property
    def basepath(self):
        return f'/sys/class/hwmon/hwmon2/pwm{self.num}'

    @property
    def path_rpm(self):
        return Path(f'/sys/class/hwmon/hwmon2/fan{self.num}_input')

    @property
    def basepath_path(self):
        return Path(self.basepath)

    @property
    def path_enable(self):
        return Path(self.basepath + '_enable')

    @property
    def enable(self):
        return bool(self.path_enable.read_text())

    @enable.setter
    def enable(self, value):
        assert isinstance(value, bool)
        self.basepath_path.write_text(str(int(value)))

    @property
    def fan_speed(self):
        """Target speed from 0-255"""
        return int(self.basepath_path.read_text())

    @fan_speed.setter
    def fan_speed(self, speed):
        """Target speed from 0-255"""
        assert 0 <= speed <= 255
        self.basepath_path.write_text(str(speed))
        assert self.fan_speed == speed

    @property
    def rpm(self):
        return int(self.path_rpm.read_text())
