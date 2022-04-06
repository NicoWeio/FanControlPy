#!/usr/bin/env python3

from fan_curve import FanCurve
import code
from pathlib import Path
import subprocess
import time

from config import MY_FANS
from fan import Fan
from temp_sensor import TempSensor


fan = MY_FANS['Front']  # for testing
tempSensor = TempSensor(1)

fanCurvePoints = [
    (70, 0),
    (75, 1),
]
fanCurve = FanCurve(fanCurvePoints)

if not fan.enable:
    print('Enabling fan')
    fan.enable = True

while True:
    try:
        calculatedSpeed = fanCurve.get_power(tempSensor.temp)

        print(f'RPM: {fan.rpm}')
        print(f'Current speed: {fan.fan_speed:.2f}')
        print(f'Current temperature: {tempSensor.temp:.1f}')
        print(f'Calculated speed: {calculatedSpeed:.2f}')

        fan.fan_speed = calculatedSpeed

        time.sleep(5)
    except KeyboardInterrupt:
        fan.enable = False
        break
