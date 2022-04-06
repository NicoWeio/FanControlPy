from fan import Fan


MY_FANS = {
    'CPU': Fan(2),
    'Front': Fan(3, min_speed=0.58),
    'Rear': Fan(5),
}
