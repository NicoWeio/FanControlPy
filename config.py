from fan import Fan
from fan_curve import FanCurve

MY_FANS = {
    'CPU': Fan(2),
    'Front': Fan(3,
                 min_speed=0.58,
                 fan_curve=FanCurve([
                     (70, 0),
                     (75, 1),
                 ]),
                 ),
    'Rear': Fan(5),
}
