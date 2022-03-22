from config import MY_FANS
import time

fan = MY_FANS['Front']
target_tol = 1

curr_min = 0
curr_max = 255
curr_tol = curr_max - curr_min

while curr_tol > target_tol:
    new_test_speed = int((curr_min + curr_max) / 2)
    # make sure the fan is spinning
    fan.spin_up_or_down_to(255, max_wait=5)
    # try out the new speed
    fan.spin_up_or_down_to(new_test_speed)
    # check if the fan is spinning
    if fan.rpm > 0:
        curr_max = new_test_speed
    else:
        curr_min = new_test_speed
    curr_tol = curr_max - curr_min

    print(f'Current min: {curr_min}, Current max: {curr_max}, Current tolerance: {curr_tol}, Current speed: {fan.fan_speed}, Target tolerance: {target_tol}')
