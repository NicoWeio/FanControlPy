from config import MY_FANS
import time

fan = MY_FANS['Front']
target_tol = 1/255

curr_min = 0.0
curr_max = 1.0

while (curr_tol := curr_max - curr_min) > target_tol:
    new_test_speed = (curr_min + curr_max) / 2
    # make sure the fan is spinning
    fan.spin_up_or_down_to(1, max_wait=5)
    # try out the new speed
    fan.spin_up_or_down_to(new_test_speed, max_wait=5)
    # check if the fan is spinning
    if fan.rpm > 0:
        curr_max = new_test_speed
    else:
        curr_min = new_test_speed

    print(f'Current min: {curr_min}, Current max: {curr_max}, Current tolerance: {curr_tol}, Current speed: {fan.fan_speed}, Target tolerance: {target_tol}')
