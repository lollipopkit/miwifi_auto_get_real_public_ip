import multiprocessing
import sys
import time as times

import utils
import requests
import re
from datetime import datetime, time


# ------------------plz fill these parameter below this line-----------------------


# Password for your Mi WiFi router admin page
password = ''
# Local router IP for your Mi router, you can find it in your phone wifi setting.
# Usually no need to edit it.
router_ip = '192.168.31.1'

# Each time you want to get ip
start_time = {
    # each day 8 AM
    time(18, 39),
    # each day 10:50 PM
    time(22, 50),
}
# Day of the week to run this script，attention: 0 is Sunday
start_day = [1, 2, 3, 4, 5, 6, 7]


# ---------------------no need to edit anything below this line--------------------


# init vars
timestamp = 0.0
should_run = False
# Listen duration, eg: this thread last 10 seconds by default
listen_time = 10


def my_print(string):
    print(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S') + '  ' + string)


def get_ip():
    global should_run
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

    print('Your Public IP: ', wan_ip, '\n')


def listen():
    # Main thread
    my_print('Main listen thread start.')
    child_process = None
    global should_run, timestamp

    while True:
        # Get current time
        current_time = datetime.now().strftime('%H:%M')
        weekday = datetime.now().strftime('%w')

        # judge whether should run
        if int(weekday) in start_day:
            for item in start_time:
                if str(item)[:-3] == current_time:
                    timestamp = times.time()
                    should_run = True
                if should_run and times.time() - timestamp > listen_time:
                    should_run = False

        # Start thread
        if should_run and child_process is None:
            my_print('Automatically start thread\n')
            child_process = multiprocessing.Process(target=get_ip)
            child_process.start()

        # Stop thread
        if not should_run and child_process is not None:
            my_print('Automatically stop thread\n')
            child_process.terminate()
            child_process.join()
            child_process = None

        # Sleep for next detection
        times.sleep(listen_time)


if __name__ == '__main__':
    try:
        arg = sys.argv
        if arg[1] == 'listen':
            try:
                listen()
            except KeyboardInterrupt:
                my_print('Stopped by user.\n')
        elif arg[1] == 'get':
            get_ip()
        else:
            print('plz enter any correct arg, not: ' + arg[1])
    except IndexError:
        print('Plz ensure that you have input any correct parameter')
