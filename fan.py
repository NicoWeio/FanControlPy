from pathlib import Path
# import subprocess
import time


class Fan:
    def __init__(self, num, name=None, min_speed=0, fan_curve=None):
        self.name = name or f'#{num}'
        self.num = num
        self.min_speed = min_speed
        self.fan_curve = fan_curve

    def __repr__(self):
        return f'<Fan "{self.name}">'

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
        # Fan speed control method:
        #         0: no fan speed control (i.e. fan at full speed)
        #         1: manual fan speed control enabled (using pwm[1-*])
        #         2+: automatic fan speed control enabled
        #         Check individual chip documentation files for automatic mode
        #         details.
        return self.path_enable.read_text().strip() == '1'

    @enable.setter
    def enable(self, value):
        assert isinstance(value, bool)
        self.basepath_path.write_text(str(int(value)))
        time.sleep(1)
        assert self.enable == value, f'{self.enable} != {value}'

    @property
    def fan_speed_internal(self):
        """Target speed from 0-255"""
        return int(self.basepath_path.read_text())

    @fan_speed_internal.setter
    def fan_speed_internal(self, speed_internal):
        """Target speed from 0-255"""
        assert 0 <= speed_internal <= 255
        self.basepath_path.write_text(str(int(speed_internal)))
        assert self.fan_speed_internal == speed_internal, f'{self.fan_speed_internal} != {speed_internal}'

    @property
    def fan_speed(self):
        """Target speed from 0-1"""
        return self.fan_speed_internal / 255

    @fan_speed.setter
    def fan_speed(self, speed):
        """Target speed from 0-1"""
        assert 0 <= speed <= 1
        # stop fan if the desired speed is below its min_speed
        actual_speed = speed if speed >= self.min_speed else 0
        self.fan_speed_internal = int(actual_speed * 255)

    @property
    def rpm(self):
        return int(self.path_rpm.read_text())

    # ---

    def spin_up_or_down_to(self, speed, wait_interval=2, min_wait=5, max_wait=15):
        """Sets target speed(0-1) and waits until it is reached"""
        assert 0 <= speed <= 1
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
