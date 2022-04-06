#!/usr/bin/env python3

from fan_curve import FanCurve
import code
from pathlib import Path
import subprocess
import time

from config import MY_FANS
from fan import Fan
from temp_sensor import TempSensor

fans = MY_FANS
tempSensor = TempSensor(1)

for fan_name, fan in fans.items():
    if not fan.enable:
        print(f"Enabling {fan_name}")
        fan.enable = True

while True:
    print(f'Current temperature: {tempSensor.temp:.1f} °C')
    for fan_name, fan in fans.items():
        if not fan.fan_curve:
            continue
        try:
            calculatedSpeed = fan.fan_curve.get_power(tempSensor.temp)

            print(f"{fan_name}: {calculatedSpeed:.0%}, {fan.rpm} RPM")

            fan.fan_speed = calculatedSpeed

            time.sleep(5)
        except KeyboardInterrupt:
            fan.enable = False
            break
