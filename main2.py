# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# vim: set foldmethod=marker commentstring=\ \ #\ %s :
#
# Author:    Taishi Matsumura
# Created:   2017-10-31
#
# Copyright (C) 2017 Taishi Matsumura
#
import sys
import time
import paho.mqtt.publish as publish
import threading
import os
import os.path
import datetime
import numpy as np
from params import *


class Beacon(threading.Thread):
    def __init__(self, username, password, host, device_id, period, message):
        super(Beacon, self).__init__()
        self.username = username
        self.password = password
        self.host = host
        self.device_id = device_id
        self.period = period
        self.message = message
        self.setDaemon(True)

    def run(self):
        time.sleep(5 * np.random.rand())
        while True:
            tm = time.time()
            data = [tm, self.message]
            payload = '{{"tm":"{0}","Beacon":"{1}"}}'.format(*data)
            print 'Beacon: {}\n'.format(payload)
            publish.single(
                    topic='{}/{}'.format(self.password, self.device_id),
                    payload=payload,
                    hostname=self.host,
                    auth={'username': self.username,
                        'password': self.password})
            time.sleep(self.period)


class EnvironmentalInformation(threading.Thread):
    def __init__(self, username, password, host, device_id, period):
        super(EnvironmentalInformation, self).__init__()
        self.username = username
        self.password = password
        self.host = host
        self.device_id = device_id
        self.period = period
        self.setDaemon(True)

    def run(self):
        time.sleep(5 * np.random.rand())
        t = 0
        dt = 0.1
        while True:
            tm = time.time()
            eiLPrs = np.random.rand() + 900 + 100*np.sin(2*np.pi*t)
            seaPrs = np.random.rand() + 1000 + 100*np.sin(2*np.pi*t)
            eiTemp = np.random.rand() + 20 + 10*np.sin(2*np.pi*t)
            eiHumi = np.random.rand() + 50 + 30*np.sin(2*np.pi*t)
            data = [tm, eiLPrs, seaPrs, eiTemp, eiHumi]
            payload = '{{"tm":"{0}","eiLPrs":{1},"seaPrs":{2},"eiTemp":{3},"eiHumi":{4}}}'.format(*data)
            print 'EnvInfo: {}\n'.format(payload)
            publish.single(
                    topic='{}/{}'.format(self.password, self.device_id),
                    payload=payload,
                    hostname=self.host,
                    auth={'username': self.username,
                        'password': self.password})
            time.sleep(self.period)
            t += dt


class DigitalSensors(threading.Thread):
    def __init__(self, username, password, host, device_id, global_period):
        super(DigitalSensors, self).__init__()
        self.username = username
        self.password = password
        self.host = host
        self.device_id = device_id
        self.global_period = global_period
        self.setDaemon(True)

    def run(self):
        time.sleep(5 * np.random.rand())
        while True:
            tm = time.time()
            d1 = np.random.randint(0, 2)
            d2 = np.random.randint(0, 2)
            d3 = np.random.randint(0, 2)
            d4 = np.random.randint(0, 2)
            d5 = np.random.randint(0, 2)
            d6 = np.random.randint(0, 2)
            d7 = np.random.randint(0, 100)
            d8 = np.random.randint(0, 2)
            data = [tm, d1, d2, d3, d4, d5, d6, d7, d8]
            payload = '{{"tm":"{0}","d1":{1},"d2":{2},"d3":{3},"d4":{4},"d5":{5},"d6":{6},"d7":{7},"d8":{8}}}'.format(*data)
            print 'Digital: {}\n'.format(payload)
            publish.single(
                    topic='{}/{}'.format(self.password, self.device_id),
                    payload=payload,
                    hostname=self.host,
                    auth={'username': self.username,
                        'password': self.password})
            time.sleep(self.global_period)


class AnalogSensors(threading.Thread):
    def __init__(self, username, password, host, device_id, global_period):
        super(AnalogSensors, self).__init__()
        self.username = username
        self.password = password
        self.host = host
        self.device_id = device_id
        self.global_period = global_period
        self.setDaemon(True)

    def run(self):
        time.sleep(5 * np.random.rand())
        t = 0
        dt = 0.1
        while True:
            tm = time.time()
            a1 = np.random.rand() + 10 + 10*np.sin(2*np.pi*t)
            a2 = np.random.rand() + 20 + 20*np.sin(2*np.pi*t)
            a3 = np.random.rand() + 30 + 30*np.sin(2*np.pi*t)
            a4 = np.random.rand() + 40 + 40*np.sin(2*np.pi*t)
            a5 = np.random.rand() + 10 + 10*np.cos(2*np.pi*t)
            a6 = np.random.rand() + 20 + 20*np.cos(2*np.pi*t)
            a7 = np.random.rand() + 30 + 30*np.cos(2*np.pi*t)
            a8 = np.random.rand() + 40 + 40*np.cos(2*np.pi*t)
            data = [tm, a1, a2, a3, a4, a5, a6, a7, a8]
            payload = '{{"tm":"{0}","a1":{1},"a2":{2},"a3":{3},"a4":{4},"a5":{5},"a6":{6},"a7":{7},"a8":{8}}}'.format(*data)
            print 'Analog: {}\n'.format(payload)
            publish.single(
                    topic='{}/{}'.format(self.password, self.device_id),
                    payload=payload,
                    hostname=self.host,
                    auth={'username': self.username,
                        'password': self.password})
            time.sleep(self.global_period)
            t += dt


class Device(object):
    def __init__(self, username, password, host, device_id, p_beacon=60, p_env=720, p_digi=60, p_ana=15):
        self.username = username
        self.password = password
        self.host = host
        self.device_id = device_id
        self.beacon = Beacon(username, password, host, device_id, p_beacon, message=device_id)
        self.envinfo = EnvironmentalInformation(username, password, host, device_id, p_env)
        self.digisnsrs = DigitalSensors(username, password, host, device_id, p_digi)
        self.anasnsrs = AnalogSensors(username, password, host, device_id, p_ana)

    def switch_on(self):
        self.beacon.start()
        self.envinfo.start()
        self.digisnsrs.start()
        self.anasnsrs.start()

class Devices(object):
    def __init__(self, n, username, password, host):
        self.n = n
        self.username = username
        self.password = password
        self.host = host
        self.devices = {}
        for i in xrange(1, n+1):
            id = '{:04d}'.format(i)
            device_id = 'IFT_ML1-YONEZAWA{}'.format(id)
            self.devices[id] = Device(username, password, host, device_id)

    def switch_on(self):
        for i in xrange(1, self.n+1):
            id = '{:04d}'.format(i)
            self.devices[id].switch_on()


if __name__ == '__main__':
    devices = Devices(4, USERNAME, PASSWORD, HOST)
    devices.switch_on()

    while True:
        c = sys.stdin.read(1)
        if c == 'e':
            sys.exit()
