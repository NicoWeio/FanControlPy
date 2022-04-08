#!/usr/bin/env python3

import code
from pathlib import Path
import subprocess
import time

from fancontrolpy.config import MY_FANS
from fancontrolpy.fan import Fan
from fancontrolpy.fan_curve import FanCurve
from fancontrolpy.temp_sensor import TempSensor

# TODO: move to config ↓
# how often to update the fan speed
INTERVAL_SECONDS = 5
# how many seconds to average over
AVG_SECONDS = 30
# calculate how many samples to average over
AVG_SAMPLES = AVG_SECONDS // INTERVAL_SECONDS
assert AVG_SAMPLES >= 2  # needed for correct array indexing


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

last_temps: list[float] = []

try:
    last_handled_temp = 0.0  # reasonable default
    while True:
        current_temp = tempSensor.temp
        last_temps = last_temps[-(AVG_SAMPLES-1):] + [current_temp]
        smooth_temp = sum(last_temps) / len(last_temps)
        print(f'Current temperature: {current_temp:.1f} °C, average: {smooth_temp:.1f} °C')
        if abs(smooth_temp - last_handled_temp) < 1:
            # print('No significant change in temperature, skipping…')
            pass
        else:
            last_handled_temp = smooth_temp
            for fan in fans:
                calculatedSpeed = fan.fan_curve.get_power(smooth_temp)
                print(f"{fan}: {calculatedSpeed:.0%}, {fan.rpm} RPM")
                try:
                    fan.fan_speed = calculatedSpeed
                except AssertionError:
                    print(f"Failed to set {fan} to {calculatedSpeed:.0%}!")
        time.sleep(INTERVAL_SECONDS)

except KeyboardInterrupt:
    print('\nExiting; resetting fans...')
    for fan in fans:
        try:
            fan.fan_speed = 1
            fan.enable = False
        except AssertionError:
            print(f'Failed to reset {fan}')
            pass
