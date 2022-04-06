#!/usr/bin/env python3

from pathlib import Path
import subprocess
import time

from fan import Fan


MY_FANS = {
    'CPU': Fan(2),
    'Front': Fan(3),
    'Rear': Fan(5),
}


def main():
    for fan_name, fan in MY_FANS.items():
        print(f'{fan_name}: {fan.fan_speed}/255, {fan.rpm} RPM')
    print('---')


while True:
    main()
    time.sleep(5)
