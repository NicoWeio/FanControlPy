from pathlib import Path
# import subprocess
import time


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
        """Target speed from 0-1"""
        return int(self.basepath_path.read_text()) / 255

    @fan_speed.setter
    def fan_speed(self, speed):
        """Target speed from 0-1"""
        assert 0 <= speed <= 1
        self.basepath_path.write_text(str(int(speed * 255)))
        assert self.fan_speed == speed

    @property
    def rpm(self):
        return int(self.path_rpm.read_text())

    # ---

    def spin_up_or_down_to(self, speed, wait_interval=2, min_wait=5, max_wait=15):
        """Sets target speed and waits until it is reached"""
        direction = 'up' if speed > self.fan_speed else 'down'

        self.fan_speed = speed
        prev_rpm = 0 if direction == 'up' else self.rpm
        next_rpm = self.rpm if direction == 'up' else 0
        wait_time = 0

        while ((next_rpm > prev_rpm if direction == 'up' else next_rpm < prev_rpm) or wait_time < min_wait) and wait_time < max_wait:
            if direction == 'down' and self.rpm == 0:
                print('Fan stopped')
                break

            print(f'Still spinning {direction}… ({prev_rpm} → {next_rpm})')
            time.sleep(wait_interval)
            wait_time += wait_interval
            prev_rpm = next_rpm
            next_rpm = self.rpm
        print(f'Done: {prev_rpm} → {next_rpm}')
