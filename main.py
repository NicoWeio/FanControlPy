#!/usr/bin/env python3

import code
from pathlib import Path
import subprocess
import time

from fancontrolpy.config import MY_FANS
from fancontrolpy.fan import Fan
from fancontrolpy.fan_curve import FanCurve
from fancontrolpy.temp_sensor import TempSensor

fans = [fan for fan in MY_FANS if fan.fan_curve]
tempSensor = TempSensor(1)

for fan in fans:
    if not fan.enable:
        print(f"Enabling {fan}")
        try:
        fan.enable = True
        except AssertionError:
            # Setting a speed might enable it, though, so don't fail here.
            print(f"Failed to enable {fan}")

try:
    last_handled_temp = 0  # reasonable default
    while True:
        temp = tempSensor.temp
        print(f'Current temperature: {temp:.1f} °C')
        if abs(temp - last_handled_temp) < 1:
            print('No significant change in temperature, skipping…')
        else:
            last_handled_temp = temp
            for fan in fans:
                calculatedSpeed = fan.fan_curve.get_power(temp)
                print(f"{fan}: {calculatedSpeed:.0%}, {fan.rpm} RPM")
                fan.fan_speed = calculatedSpeed
        time.sleep(10)

except KeyboardInterrupt:
    print('\nExiting; resetting fans...')
    for fan in fans:
        try:
            fan.fan_speed = 1
            fan.enable = False
        except AssertionError:
            print(f'Failed to reset {fan}')
            pass
