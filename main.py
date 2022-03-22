#!/usr/bin/env python3

import code
from pathlib import Path
import subprocess

from fan import Fan


MY_FANS = {
    'CPU': Fan(2),
    'Front': Fan(3),
    'Rear': Fan(5),
}

for fan_name, fan in MY_FANS.items():
    print(f'→ {fan_name}: {fan.fan_speed}')

    print(f'Speed before: {fan.fan_speed}')
    print(f'Enable before: {fan.enable}')
    # fan.enable = False
    fan.fan_speed = 0
    print(f'Speed after: {fan.fan_speed}')
    print(f'Enable after: {fan.enable}')

code.interact(local=locals())
