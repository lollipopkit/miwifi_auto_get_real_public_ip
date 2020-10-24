#!/usr/bin/env python
# coding=utf-8
# -*- coding: utf-8 -*-

# 小米路由器远程管理 API

import random
import math
import time
import hashlib
import json

import requests


def utf8_encode(string):
    return string.encode('utf-8')


class MiWiFi():
    """
    docstring for MiWiFi
    """

    def __init__(self, password=None):
        super(MiWiFi, self).__init__()

        self.deviceId = None
        self.type = '0'
        self.nonce = None
        self.password = password
        self.stok = None
        self.cookies = None

        # 小米路由器首页
        self.URL_ROOT = "http://miwifi.com"
        # 小米路由器登录页面
        self.URL_LOGIN = "%s/cgi-bin/luci/api/xqsystem/login" % self.URL_ROOT
        # 小米路由器当前设备清单页面，登录后取得 stok 值才能完成拼接
        self.URL_ACTION = None
        self.URL_DeviceListDaemon = None

    def nonceCreat(self, miwifi_device_id):
        """
        docstring for nonceCreat()
        模仿小米路由器的登录页面，计算 hash 所需的 nonce 值
        """
        self.deviceId = miwifi_device_id
        miwifi_type = self.type
        miwifi_time = str(int(math.floor(time.time())))
        miwifi_random = str(int(math.floor(random.random() * 10000)))
        self.nonce = '_'.join([miwifi_type, miwifi_device_id, miwifi_time, miwifi_random])
        print('nonce: ', self.nonce)

        return self.nonce

    def oldPwd(self, password, key):
        """
        docstring for oldPwd()
        模仿小米路由器的登录页面，计算密码的 hash
        """
        encoded_nonce = utf8_encode(self.nonce)
        encoded_pwd_key = utf8_encode(password + key)
        hash_content = encoded_nonce + utf8_encode(hashlib.sha1(encoded_pwd_key).hexdigest())
        pwd = hashlib.sha1(hash_content)
        self.password = pwd.hexdigest()
        print('pwd: ', self.password)

        return self.password

    def login(self, device_id, password, key):
        """
        docstring for login()
        登录小米路由器，并取得对应的 cookie 和用于拼接 URL 所需的 stok
        """
        nonce = self.nonceCreat(device_id)
        password = self.oldPwd(password, key)
        payload = {'username': 'admin', 'logtype': '2', 'password': password, 'nonce': nonce}

        try:
            r = requests.post(self.URL_LOGIN, data=payload)
            stok = json.loads(r.text).get('url').split('=')[1].split('/')[0]
        except Exception as e:
            raise e

        self.stok = stok
        self.cookies = r.cookies
        self.URL_ACTION = "%s/cgi-bin/luci/;stok=%s/api" % (self.URL_ROOT, self.stok)
        self.URL_DeviceListDaemon = "%s/xqsystem/device_list" % self.URL_ACTION
        return stok, r.cookies

    def listDevice(self):
        """
        docstring for listDevice()
        列出小米路由器上当前的设备清单
        """
        if self.URL_DeviceListDaemon is not None and self.cookies is not None:
            try:
                r = requests.get(self.URL_DeviceListDaemon, cookies=self.cookies)
                # print json.dumps(json.loads(r.text), indent=4)
                return json.loads(r.text).get('list')
            except Exception as e:
                raise e
        else:
            return 'plz login first'

    def runAction(self, action):
        """
        docstring for runAction()
        run a custom action like "pppoe_status", "pppoe_stop", "pppoe_start" ...
        """
        if self.URL_DeviceListDaemon is not None and self.cookies is not None:
            try:
                r = requests.get('%s/xqnetwork/%s' % (self.URL_ACTION, action), cookies=self.cookies)
                return json.loads(r.text)
            except Exception as e:
                raise e
        else:
            return 'plz login first'
