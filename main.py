#!/usr/bin/env python3

from fan_curve import FanCurve
import code
from pathlib import Path
import subprocess
import time

from fan import Fan
from temp_sensor import TempSensor

MY_FANS = {
    'CPU': Fan(2),
    'Front': Fan(3),
    'Rear': Fan(5),
}

fan = MY_FANS['Front']  # for testing
tempSensor = TempSensor(1)

fanCurvePoints = [
    (50, 0.5),
    (100, 1),
]
fanCurve = FanCurve(fanCurvePoints)

if not fan.enable:
    print('Enabling fan')
    fan.enable = True

while True:
    calculatedSpeed = fanCurve.get_power(tempSensor.temp)

    print(f'RPM: {fan.rpm}')
    print(f'Current speed: {fan.fan_speed:.2f}')
    print(f'Current temperature: {tempSensor.temp}')
    print(f'Calculated speed: {calculatedSpeed:.2f}')

    fan.fan_speed = calculatedSpeed

    time.sleep(5)
