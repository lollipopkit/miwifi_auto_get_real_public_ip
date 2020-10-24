import utils
import requests
import re

# plz fill these two with your own miwifi_router login password and local router ip
password = ''
router_ip = '192.168.31.1'

# get device_id and key for login()
req = requests.get('http://{}/cgi-bin/luci/web/home'.format(router_ip))
html_body = req.text
device_id = re.findall("(?<=deviceId = ').*(?=';)", html_body)[0]
key = re.findall("(?<=key: ').*(?=',)", html_body)[0]

# login for getting wan_ip(Public IP)
mi_wifi = utils.MiWiFi(password=password)
mi_wifi.login(device_id, password, key)
pppoe_dict = mi_wifi.runAction('pppoe_status')
wan_ip = pppoe_dict['ip']['address']

print('Your Public IP: ', wan_ip)
