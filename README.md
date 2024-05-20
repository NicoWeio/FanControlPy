# Installation
```sh
# cd /etc/systemd/system
# modify the /path/to/FanControlPy/main.py in the fancontrolpy_daemon.service file
sudo ln -s '/path/to/FanControlPy/fancontrolpy_daemon.service' fancontrolpy_daemon.service  # or move it there
sudo systemctl enable fancontrolpy_daemon.service
sudo systemctl start fancontrolpy_daemon.service
```

---

# Why?
Because I dislike shell scripts.
They're cluttered and not easily hackable.

# How?
For reference:
- [pwmconfig (local file)](/usr/bin/pwmconfig)
- https://github.com/lm-sensors/lm-sensors/blob/master/prog/pwm/fancontrol
