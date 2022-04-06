from config import MY_FANS
import time

for fan_name, fan in MY_FANS.items():
    print(f'→ Now checking {fan_name}')

    fan.spin_up_or_down_to(255)

    # remember the maximum rpm
    max_rpm = fan.rpm

    # now decrease fan.fan_speed until fan.rpm is 0
    while fan.rpm > 0:
        print(f'Current speed: {(fan.fan_speed/255):.0%}, RPM: {fan.rpm}')

        step_size = 32 if fan.rpm > (max_rpm / 2) else 16
        wait_dur = 1 if fan.rpm > (max_rpm / 2) else 3
        new_speed = fan.fan_speed - step_size
        if new_speed < 0:
            new_speed = 0
            print("The fan didn't stop.")
            break
        fan.spin_up_or_down_to(new_speed, wait_interval=wait_dur)

    min_fan_speed = fan.fan_speed

    print(f'→ {fan_name} has a min speed of {min_fan_speed}')
