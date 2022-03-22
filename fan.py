from pathlib import Path
# import subprocess


class Fan:
    def __init__(self, basepath):
        # basepath is e.g. /sys/class/hwmon/hwmon2/pwm3
        assert basepath.startswith('/sys/class/hwmon/hwmon')
        self.basepath = Path(basepath)

    @property
    def enable(self):
        return bool(Path(str(self.basepath) + '_enable').read_text())

    @enable.setter
    def enable(self, value):
        assert isinstance(value, bool)
        Path(str(self.basepath) + '_enable').write_text(str(int(value)))

    @property
    def fan_speed(self):
        return int(self.basepath.read_text())

    @fan_speed.setter
    def fan_speed(self, speed):
        assert 0 <= speed <= 255
        self.basepath.write_text(str(speed))
        assert self.fan_speed == speed
