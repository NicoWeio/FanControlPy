import numpy as np


class FanCurve:
    def __init__(self, points):
        # points are tuples of (temperature in °C, power as float between 0 and 1)

        # validate points
        for point in points:
            temp, power = point
            assert 0 <= temp <= 100  # ?
            assert 0 <= power <= 1

        self.points = points

    def get_power(self, temperature):
        """returns the power in % for a given temperature"""
        temperatures = np.array([point[0] for point in self.points])
        powers = np.array([point[1] for point in self.points])

        return np.interp(temperature, temperatures, powers)
