#!/usr/bin/env python3

from fan_curve import FanCurve
import code
from pathlib import Path
import subprocess
import time

from config import MY_FANS
from fan import Fan
from temp_sensor import TempSensor

fans = [fan for fan in MY_FANS if fan.fan_curve]
tempSensor = TempSensor(1)

for fan in fans:
    if not fan.enable:
        print(f"Enabling {fan}")
        fan.enable = True

try:
    while True:
        print(f'Current temperature: {tempSensor.temp:.1f} °C')
        for fan in fans:
            calculatedSpeed = fan.fan_curve.get_power(tempSensor.temp)
            print(f"{fan}: {calculatedSpeed:.0%}, {fan.rpm} RPM")
            fan.fan_speed = calculatedSpeed
        time.sleep(5)

except KeyboardInterrupt:
    print('\nExiting; resetting fans...')
    for fan in fans:
        try:
            fan.fan_speed = 1
            fan.enable = False
        except AssertionError:
            print(f'Failed to reset {fan}')
            pass
