# Intro
For Internet penetration. Only Mi WiFi Router.

小米路由器自动获取真实公网IP，以供内网穿透。

# Attention
Plz specific `password, start_day/time, router_ip` in `main.py` before run.

使用前请先修改`main.py`内`password, start_day/time, router_ip`值。

# Usage
run `python3 main.py listen` in terminal for servers(such as your Raspberry Pi which you want to get real ip).

使用以上命令可以使本脚本持续运行于服务器（比如树莓派）中。

or run `python3 main.py get` to get the ip only once.

使用以上命令仅获取一次IP。


# TODO
- [ ] Web hook for notification when IP change
- [x] Thread mode for server run
- [x] Optional parameter for shell command

# Dependency
`Python 3` and `requests` library

`pip3 install requests` for installing `requests`

# Thanks
[Py Mi WiFi](https://github.com/sbilly/pyMiWiFi)

utils.py partly from this repo.

# License
```
LollipopKit 2020
Apache License 2.0
```