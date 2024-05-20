# NOTE: separate from config.py so Fan can import it without circular imports
from .fan import Fan
from .fan_curve import FanCurve

MY_FANS = [
    Fan(
        num=2,
        name="CPU",
        min_speed=0,
        fan_curve=FanCurve([
            (60, 0),  # still spinning at 0%
            # (70, 0.4),
            (80, 1),
        ]),
    ),
    Fan(
        num=3,
        name="Front",
        # min_speed=0.58,
        min_speed=0.75,
        fan_curve=FanCurve([
            (70, 0),
            (75, 1),
        ]),
    ),
    Fan(
        num=5,
        name="Rear",
        min_speed=0.4,
        fan_curve=FanCurve([
            (50, 0),
            (75, 1),
        ]),
    ),
]
