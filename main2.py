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
import numpy as np
from params import *


class Sensor(object):
    def __init__(self):
        self.sensor_name = 'Sensor'

    def run(self):
        time.sleep(5 * np.random.rand())
        while True:
            self._make_data()
            self._send_data()
            time.sleep(self.period)

    def _make_data(self):
        pass

    def _send_data(self):
        try:
            publish.single(topic='{}/{}'.format(self.password, self.device_id),
                    payload=self.payload, hostname=self.host,
                    auth={'username': self.username, 'password': self.password})
            print '{}: {}\n'.format(self.sensor_name, self.payload)
        except:
            print '{}: The payload was not send.'.format(self.sensor_name)


class Beacon(Sensor, threading.Thread):
    def __init__(self, username, password, host, device_id, period, message):
        super(Beacon, self).__init__()
        super(Sensor, self).__init__()
        self.sensor_name = 'Beacon'
        self.username = username
        self.password = password
        self.host = host
        self.device_id = device_id
        self.period = period
        self.message = message
        self.setDaemon(True)

    def _make_data(self):
        data = [time.time(), self.message]
        self.payload = '{{"tm":"{0}","Beacon":"{1}"}}'.format(*data)


class EnvironmentalInformation(Sensor, threading.Thread):
    def __init__(self, username, password, host, device_id, period):
        super(EnvironmentalInformation, self).__init__()
        super(Sensor, self).__init__()
        self.sensor_name = 'EnvInfo'
        self.username = username
        self.password = password
        self.host = host
        self.device_id = device_id
        self.period = period
        self.t = 0
        self.dt = 0.1
        self.setDaemon(True)

    def _make_data(self):
        eiLPrs = np.random.rand() + 900 + 100*np.sin(2*np.pi*self.t)
        seaPrs = np.random.rand() + 1000 + 100*np.sin(2*np.pi*self.t)
        eiTemp = np.random.rand() + 20 + 10*np.sin(2*np.pi*self.t)
        eiHumi = np.random.rand() + 50 + 30*np.sin(2*np.pi*self.t)
        self.t += self.dt
        data = [time.time(), eiLPrs, seaPrs, eiTemp, eiHumi]
        self.payload = '{{"tm":"{0}","eiLPrs":{1},"seaPrs":{2},"eiTemp":{3},"eiHumi":{4}}}'.format(*data)


class DigitalSensors(Sensor, threading.Thread):
    def __init__(self, username, password, host, device_id, port_ids, period):
        super(DigitalSensors, self).__init__()
        super(Sensor, self).__init__()
        self.sensor_name = 'Digital sensor'
        self.username = username
        self.password = password
        self.host = host
        self.device_id = device_id
        self.port_ids = port_ids
        self.period = period
        self.setDaemon(True)

    def _make_data(self):
        data = ['"tm":{0}'.format(time.time())]
        for port_id in self.port_ids:
            data.append('"d{0}":{1}'.format(port_id, np.random.randint(0, 2)))
        self.payload = '{{{0}}}'.format(','.join(data))


class DigitalCounters(object):
    def __init__(self, username, password, host, device_id, port_ids, periods):
        self.port_ids = port_ids
        self.periods = periods
        self.counters = {}
        for i, (port_id, period) in enumerate(zip(port_ids, periods)):
            self.counters[i] = DigitalCounter(username, password, host, device_id, port_id, period)

    def run(self):
        for counter in self.counters.values():
            counter.start()


class DigitalCounter(Sensor, threading.Thread):
    def __init__(self, username, password, host, device_id, port_id, period):
        super(DigitalCounter, self).__init__()
        super(Sensor, self).__init__()
        self.sensor_name = 'Digital counter'
        self.username = username
        self.password = password
        self.host = host
        self.device_id = device_id
        self.port_id = port_id
        self.period = period
        self.setDaemon(True)

    def _make_data(self):
        self.payload = '{{"tm":"{0}","d{1}":{2}}}'.format(time.time(), self.port_id, np.random.randint(0, 50))


class DigitalElements(object):
    def __init__(self, username, password, host, device_id, global_period, periods=8*[0]):
        sensor_ids = [i+1 for i, p in enumerate(periods) if p==0]
        counter_ids = list(set(xrange(1, 9)) - set(sensor_ids))
        counter_periods = [p for p in periods if p!=0]
        self.sensors = DigitalSensors(username, password, host, device_id, sensor_ids, global_period)
        self.counters = DigitalCounters(username, password, host, device_id, counter_ids, counter_periods)

    def run(self):
        self.sensors.start()
        self.counters.run()


class AnalogSensors(Sensor, threading.Thread):
    def __init__(self, username, password, host, device_id, period):
        super(AnalogSensors, self).__init__()
        super(Sensor, self).__init__()
        self.sensor_name = 'Analog sensor'
        self.username = username
        self.password = password
        self.host = host
        self.device_id = device_id
        self.period = period
        self.t = 0
        self.dt = 0.1
        self.setDaemon(True)

    def _make_data(self):
        a1 = np.random.rand() + 10 + 10*np.sin(2*np.pi*self.t)
        a2 = np.random.rand() + 20 + 20*np.sin(2*np.pi*self.t)
        a3 = np.random.rand() + 30 + 30*np.sin(2*np.pi*self.t)
        a4 = np.random.rand() + 40 + 40*np.sin(2*np.pi*self.t)
        a5 = np.random.rand() + 10 + 10*np.cos(2*np.pi*self.t)
        a6 = np.random.rand() + 20 + 20*np.cos(2*np.pi*self.t)
        a7 = np.random.rand() + 30 + 30*np.cos(2*np.pi*self.t)
        a8 = np.random.rand() + 40 + 40*np.cos(2*np.pi*self.t)
        self.t += self.dt
        data = [time.time(), a1, a2, a3, a4, a5, a6, a7, a8]
        self.payload = '{{"tm":"{0}","a1":{1},"a2":{2},"a3":{3},"a4":{4},"a5":{5},"a6":{6},"a7":{7},"a8":{8}}}'.format(*data)


class Device(object):
    def __init__(self, username, password, host, device_id, p_beacon=BEACON_PERIOD, p_env=ENV_PERIOD, p_digi=DIGITAL_SENSOR_PERIOD, p_ana=15):
        self.username = username
        self.password = password
        self.host = host
        self.device_id = device_id
        self.beacon = Beacon(username, password, host, device_id, p_beacon, message=device_id)
        self.envinfo = EnvironmentalInformation(username, password, host, device_id, p_env)
        self.digital_elems = DigitalElements(username, password, host, device_id, global_period=p_digi, periods=DIGITAL_COUNTER_PERIODS)
        self.anasnsrs = AnalogSensors(username, password, host, device_id, p_ana)

    def switch_on(self):
        self.beacon.start()
        self.envinfo.start()
        self.digital_elems.run()
        self.anasnsrs.start()


class Devices(object):
    def __init__(self, n, username, password, host):
        self.n = n
        self.username = username
        self.password = password
        self.host = host
        self.devices = {}
        for i in xrange(1, n+1):
            device_id = 'IFT_ML1-YONEZAWA{}'.format('{:04d}'.format(i))
            self.devices[i] = Device(username, password, host, device_id)

    def switch_on(self):
        for i in xrange(1, self.n+1):
            self.devices[i].switch_on()


if __name__ == '__main__':
    devices = Devices(N_DEVICE, USERNAME, PASSWORD, HOST)
    devices.switch_on()

    while True:
        c = sys.stdin.read(1)
        if c == 'e':
            sys.exit()
