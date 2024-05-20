import logging
import time
from pathlib import Path

from .config import HWMON_PATH
from .fan_curve import FanCurve


class Fan:
    def __init__(self, num: int, name: str | None = None, min_speed: float = 0, fan_curve: FanCurve | None = None):
        self.name = name or f'#{num}'
        self.num = num
        self.min_speed = min_speed
        self.fan_curve = fan_curve

    def __repr__(self):
        return f'<Fan "{self.name}" (#{self.num})>'

    @property
    def path_base(self) -> Path:
        return HWMON_PATH / f'pwm{self.num}'

    @property
    def path_rpm(self) -> Path:
        return HWMON_PATH / f'fan{self.num}_input'

    @property
    def path_enable(self) -> Path:
        # return self.basename.with_name(self.basename.name + '_enable')
        return HWMON_PATH / f'pwm{self.num}_enable'

    @property
    def enabled(self) -> bool:
        # Fan speed control method:
        #         0: no fan speed control (i.e. fan at full speed)
        #         1: manual fan speed control enabled (using pwm[1-*])
        #         2+: automatic fan speed control enabled
        #         Check individual chip documentation files for automatic mode
        #         details.
        return self.path_enable.read_text().strip() == '1'

    @enabled.setter
    def enabled(self, value):
        assert isinstance(value, bool)
        logging.debug(f"setting enabled to {str(int(value))}")
        self.path_enable.write_text(str(int(value)))
        for _ in range(3):
            if self.enabled == value:
                break
            logging.debug(f"waiting for enabled to be {value}")
            time.sleep(1)

        assert self.enabled == value, f'{self.enabled} != {value}'  # FIXME: other code expects this to raise an AssertionError

    @property
    def fan_speed_internal(self):
        """Target speed from 0-255"""
        return int(self.path_base.read_text())

    @fan_speed_internal.setter
    def fan_speed_internal(self, speed_internal):
        """Target speed from 0-255"""
        assert 0 <= speed_internal <= 255
        self.path_base.write_text(str(int(speed_internal)))
        assert self.fan_speed_internal == speed_internal, f'{self.fan_speed_internal} != {speed_internal}'

    @property
    def fan_speed(self):
        """Target speed from 0-1"""
        return self.fan_speed_internal / 255

    @fan_speed.setter
    def fan_speed(self, speed):
        """Target speed from 0-1"""
        assert 0 <= speed <= 1

        # If the desired speed is below its min_speed…
        # A) stop the fan
        # actual_speed = speed if speed >= self.min_speed else 0
        # OR
        # B) keep it spinning at min_speed
        # actual_speed = max(speed, self.min_speed)
        # OR
        # C) keep it spinning at min_speed only if speed > 0
        actual_speed = max(speed, self.min_speed) if speed > 0 else 0

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
                logging.info("Fan stopped")
                break

            logging.info(f"Still spinning {direction}… ({prev_rpm} → {next_rpm})")
            time.sleep(wait_interval)
            wait_time += wait_interval
            prev_rpm = next_rpm
            next_rpm = self.rpm
        logging.info(f"Done: {prev_rpm} → {next_rpm}")
