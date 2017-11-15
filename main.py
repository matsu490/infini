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
import random
import csv
import os
import os.path
import datetime
from params import *


class Device(threading.Thread):
    def __init__(self, username, password, device_id, message, host,
            period=15, port=1883,
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


class Devices(object):
    def __init__(self, n, period, host, analog=False, csv=False):
        self.n = n
        self.devices = {}
        for i in xrange(1, n+1):
            line = "self.devices['d{0:04d}'] = Device('MG00017', '4w2P47Ph', 'IFT_ML1-YONEZAWA{1:04d}', '検証機{2:04d}', host, period={3}, analog={4}, csv={5})".format(i, i, i, period, analog, csv)
            exec(line)

    def start(self):
        for i in xrange(1, self.n+1):
            time.sleep(1 * random.random())
            line = "self.devices['d{0:04d}'].start()".format(i)
            exec(line)

if __name__ == '__main__':
    ds = Devices(n=100, period=15, host=host, analog=True, csv=True)
    ds.start()

    while True:
        c = sys.stdin.read(1)
        if c == 'e':
            sys.exit()
