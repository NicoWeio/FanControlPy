from fan import Fan
from fan_curve import FanCurve

MY_FANS = [
    Fan(
        num=2,
        name="CPU"
    ),
    Fan(
        num=3,
        name="Front",
        min_speed=0.58,
        fan_curve=FanCurve([
            (70, 0),
            (75, 1),
        ]),
    ),
    Fan(
        num=5,
        name="Rear"
    ),
]
