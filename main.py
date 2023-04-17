#!/usr/bin/env python3

import logging
import time
import click

from fancontrolpy.config import MY_FANS
from fancontrolpy.temp_sensor import TempSensor

# TODO: move to config ↓
# how often to update the fan speed
INTERVAL_SECONDS = 5
# how many seconds to average over
AVG_SECONDS = 30
# calculate how many samples to average over
AVG_SAMPLES = AVG_SECONDS // INTERVAL_SECONDS
assert AVG_SAMPLES >= 2  # needed for correct array indexing


@click.command()
@click.option('--loglevel', default='INFO', help="Set the log level", type=click.Choice(['debug', 'info', 'warning', 'error', 'critical']))
def main(loglevel):
    logging.basicConfig(level=loglevel.upper())

    fans = [fan for fan in MY_FANS if fan.fan_curve]
    tempSensor = TempSensor(1)

    for fan in fans:
        if not fan.enable:
            logging.info(f"Enabling {fan}")
            try:
                fan.enable = True
            except AssertionError:
                # Setting a speed might enable it, though, so don't fail here.
                logging.error(f"Failed to enable {fan}")
    logging.info("Initialization complete")

    last_temps: list[float] = []

    try:
        last_handled_temp = 0.0  # reasonable default
        while True:
            current_temp = tempSensor.temp
            last_temps = last_temps[-(AVG_SAMPLES-1):] + [current_temp]
            smooth_temp = sum(last_temps) / len(last_temps)
            logging.debug(f"Current temperature: {current_temp:.1f} °C, average: {smooth_temp:.1f} °C")
            if abs(smooth_temp - last_handled_temp) < 1:
                # logging.debug('No significant change in temperature, skipping…')
                pass
            else:
                last_handled_temp = smooth_temp
                for fan in fans:
                    calculatedSpeed = fan.fan_curve.get_power(smooth_temp)
                    logging.debug(f"{fan}: {calculatedSpeed:.0%}, {fan.rpm} RPM")
                    try:
                        fan.fan_speed = calculatedSpeed
                    except AssertionError:
                        logging.error(f"Failed to set {fan} to {calculatedSpeed:.0%}!")
                        if not fan.enable:
                            logging.warning(f"Trying to re-enable {fan}")
                            try:
                                fan.enable = True
                            except AssertionError:
                                logging.error(f"Failed to enable {fan}")
            time.sleep(INTERVAL_SECONDS)

    except KeyboardInterrupt:
        logging.info("\nExiting; resetting fans...")
        for fan in fans:
            try:
                fan.fan_speed = 1
                fan.enable = False
            except AssertionError:
                logging.error(f"Failed to reset {fan}")
                pass
        logging.info("Reset complete")


if __name__ == '__main__':
    main()
