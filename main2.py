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
    def __init__(self, period):
        super(Beacon, self).__init__()
        self.period = period
        self.message = DEVICE_ID
        self.setDaemon(True)

    def run(self):
        while True:
            tm = time.time()
            data = [tm, self.message]
            payload = '{{"tm":"{0}","Beacon":"{1}"}}'.format(*data)
            print 'Beacon: {}\n'.format(payload)
            publish.single(topic=TOPIC,
                    payload=payload,
                    hostname=HOST,
                    auth={'username': USERNAME, 'password': PASSWORD})
            time.sleep(self.period)


class EnvironmentalInformation(threading.Thread):
    def __init__(self, period):
        super(EnvironmentalInformation, self).__init__()
        self.period = period
        self.setDaemon(True)

    def run(self):
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
            publish.single(topic=TOPIC,
                    payload=payload,
                    hostname=HOST,
                    auth={'username': USERNAME, 'password': PASSWORD})
            time.sleep(self.period)
            t += dt


class DigitalSensors(threading.Thread):
    def __init__(self, global_period):
        super(DigitalSensors, self).__init__()
        self.global_period = global_period
        self.setDaemon(True)

    def run(self):
        while True:
            tm = time.time()
            d1 = np.random.randint(0, 2)
            d2 = np.random.randint(0, 2)
            d3 = np.random.randint(0, 2)
            d4 = np.random.randint(0, 2)
            d5 = np.random.randint(0, 2)
            d6 = np.random.randint(0, 2)
            d7 = np.random.randint(0, 2)
            d8 = np.random.randint(0, 2)
            data = [tm, d1, d2, d3, d4, d5, d6, d7, d8]
            payload = '{{"tm":"{0}","d1":{1},"d2":{2},"d3":{3},"d4":{4},"d5":{5},"d6":{6},"d7":{7},"d8":{8}}}'.format(*data)
            print 'Digital: {}\n'.format(payload)
            publish.single(topic=TOPIC,
                    payload=payload,
                    hostname=HOST,
                    auth={'username': USERNAME, 'password': PASSWORD})
            time.sleep(self.global_period)


class DigitalCounter(threading.Thread):
    def __init__(self, global_period):
        super(DigitalCounter, self).__init__()
        self.global_period = global_period
        self.setDaemon(True)

    def run(self):
        while True:
            tm = time.time()
            d7 = np.random.randint(0, 2)
            data = [tm, a7]
            payload = '{{"tm":"{0}","d7":{7}}}'.format(*data)
            print 'DigiCntr: {}\n'.format(payload)
            publish.single(topic=TOPIC,
                    payload=payload,
                    hostname=HOST,
                    auth={'username': USERNAME, 'password': PASSWORD})
            time.sleep(self.global_period)


class AnalogSensors(threading.Thread):
    def __init__(self, global_period):
        super(AnalogSensors, self).__init__()
        self.global_period = global_period
        self.setDaemon(True)

    def run(self):
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
            publish.single(topic=TOPIC,
                    payload=payload,
                    hostname=HOST,
                    auth={'username': USERNAME, 'password': PASSWORD})
            time.sleep(self.global_period)
            t += dt


class Device(threading.Thread):
    def __init__(self, username, password, device_id, message, host, port=1883,
            beacon_period=60, env_period=720, global_digital_period=60,
            analog=False, csv=False, save_dir='./MG2_send_data/'):
        super(Device, self).__init__()
        self.period = period
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.device_id = device_id
        self.topic = '%s/%s' % (password, device_id)
        self.message = message
        self.analog = analog
        self.csv = csv
        self.save_dir = save_dir
        self.init_csv()
        self.setDaemon(True)

    def run(self):
        while True:
            tm = time.time()
            if self.analog:
                data = [tm, '300.00', '2.00', '3.00', '4.00', '5.00', '6.00', '7.00', '8.00', self.message]
                payload = '{{"tm":"{0}","a1":{1},"a2":{2},"a3":{3},"a4":{4},"a5":{5},"a6":{6},"a7":{7},"a8":{8},"msg":"{9}"}}'.format(*data)
            else:
                data = [tm, self.message]
                payload = '{{"tm":"{0}","msg":"{1}"}}'.format(*data)
            publish.single(topic='%s/%s' % (self.password, self.device_id),
                    payload=payload,
                    hostname=self.host,
                    auth={'username': self.username, 'password': self.password})
            if self.csv:
                d = datetime.datetime.fromtimestamp(tm)
                data[0] = '{0}-{1}-{2} {3:02d}:{4:02d}:{5:02d}.{6}'.format(d.year, d.month, d.day, d.hour, d.minute, d.second, str(round(1e-6 * d.microsecond, 2))[2:])
                with open('{0}{1}.csv'.format(self.save_dir, self.device_id), 'a') as f:
                    writer = csv.writer(f, lineterminator=',\n')
                    writer.writerow(data)
            print tm, self.message
            time.sleep(self.period)

    def init_csv(self):
        if self.csv:
            if not os.path.exists(self.save_dir):
                os.mkdir(self.save_dir)
            with open('{0}{1}.csv'.format(self.save_dir, self.device_id), 'w') as f:
                writer = csv.writer(f, lineterminator='\n')
                if self.analog:
                    header = ['tm','a1','a2','a3','a4','a5','a6','a7','a8','msg']
                else:
                    header = ['tm','msg']
                writer.writerow(header)


if __name__ == '__main__':
    beacon = Beacon(period=60)
    envinfo = EnvironmentalInformation(period=720)
    digisnsr = DigitalSensors(global_period=60)
    beacon.start()
    envinfo.start()
    digisnsr.start()

    while True:
        c = sys.stdin.read(1)
        if c == 'e':
            sys.exit()
