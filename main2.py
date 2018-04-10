# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# vim: set foldmethod=marker commentstring=\ \ #\ %s :
#
# Author:    Taishi Matsumura
# Created:   2017-10-31
#
# Copyright (C) 2017 Taishi Matsumura
#
import os
import sys
import csv
import time
import datetime
import paho.mqtt.publish as publish
import threading
import numpy as np
from params import *


class Sensor(object):
    def __init__(self, name, device_id):
        self.sensor_name = name
        self.device_id = device_id
        self.header = []
        self.logfile_path = ''

    def _init_logfile(self):
        self._make_logdir()
        self.logfile_path = './Logs/{}/{}_{}.csv'.format(self.device_id, self.sensor_name, self._timestamp())
        self._make_logfile(self.logfile_path, self.header + ['is_err'])

    def _timestamp(self):
        d = datetime.datetime.fromtimestamp(time.time())
        return '{0}{1:02d}{2:02d}{3:02d}{4:02d}{5:02d}'.format(d.year, d.month, d.day, d.hour, d.minute, d.second)

    def _make_logdir(self):
        try:
            os.mkdir('./Logs/{}'.format(self.device_id))
        except:
            pass

    def _logging(self, is_err):
        d = datetime.datetime.fromtimestamp(self.data[0])
        dtime = '{0}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}.{6}'.format(d.year, d.month, d.day, d.hour, d.minute, d.second, str(round(1e-6 * d.microsecond, 2))[2:])
        line = [dtime] + self.data[1:] + [is_err]
        try:
            self._write_log(self.logfile_path, line)
        except IOError:
            print 'The log was not written because the logfile is open by, maybe, MS Excel.'
            temp_logfile_path = os.path.splitext(self.logfile_path)[0] + '.tmp'
            self._make_logfile(temp_logfile_path, self.header + ['is_err'])
            self._write_log(temp_logfile_path, line)

    def _make_logfile(self, file_path, line):
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                writer = csv.writer(f, lineterminator='\n')
                writer.writerow(line)

    def _write_log(self, file_path, line):
        with open(file_path, 'a') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(line)

    def run(self):
        time.sleep(5 * np.random.rand())
        while True:
            self._make_sensor_data()
            self._send_sensor_data()
            time.sleep(self.period)

    def _make_sensor_data(self):
        pass

    def _send_sensor_data(self):
        try:
            publish.single(topic='{}/{}'.format(self.password, self.device_id),
                    payload=self.payload, hostname=self.host,
                    auth={'username': self.username, 'password': self.password})
            self._logging(0)
            print '{}: {}\n'.format(self.sensor_name, self.payload)
        except:
            self._logging(1)
            print '{}: The payload was not send.'.format(self.sensor_name)


class Beacon(Sensor, threading.Thread):
    def __init__(self, name, username, password, host, device_id, period, beacon):
        super(Beacon, self).__init__(name, device_id)
        super(Sensor, self).__init__()
        self.username = username
        self.password = password
        self.host = host
        self.device_id = device_id
        self.period = period
        self.beacon = beacon
        self.header = ['time', 'beacon']
        self._init_logfile()
        self.setDaemon(True)

    def _make_sensor_data(self):
        tm = round(time.time(), 2)
        self.data = [tm, self.beacon]
        self.payload = '{{"tm":"{0}","Beacon":"{1}"}}'.format(*self.data)


class EnvironmentalInformation(Sensor, threading.Thread):
    def __init__(self, name, username, password, host, device_id, period):
        super(EnvironmentalInformation, self).__init__(name, device_id)
        super(Sensor, self).__init__()
        self.username = username
        self.password = password
        self.host = host
        self.device_id = device_id
        self.period = period
        self.t = 0
        self.dt = 0.1
        self.header = ['time', 'eiTemp', 'eiHumi', 'eiLPrs', 'seaPrs']
        self._init_logfile()
        self.setDaemon(True)

    def _make_sensor_data(self):
        tm = round(time.time(), 2)
        eiTemp = round(np.random.rand() + 20   +  10*np.sin(2*np.pi*self.t), 2)
        eiHumi = round(np.random.rand() + 50   +  30*np.sin(2*np.pi*self.t), 2)
        eiLPrs = round(np.random.rand() + 900  + 100*np.sin(2*np.pi*self.t), 2)
        seaPrs = round(np.random.rand() + 1000 + 100*np.sin(2*np.pi*self.t), 2)
        self.t += self.dt
        self.data = [tm, eiTemp, eiHumi, eiLPrs, seaPrs]
        self.payload = '{{"tm":"{0}","eiTemp":{1},"eiHumi":{2},"eiLPrs":{3},"seaPrs":{4}}}'.format(*self.data)


class DigitalSensors(Sensor, threading.Thread):
    def __init__(self, name, username, password, host, device_id, port_ids, period):
        super(DigitalSensors, self).__init__(name, device_id)
        super(Sensor, self).__init__()
        self.username = username
        self.password = password
        self.host = host
        self.device_id = device_id
        self.port_ids = port_ids
        self.period = period
        self.header = ['time'] + ['d{}'.format(port_id) for port_id in port_ids]
        self._init_logfile()
        self.setDaemon(True)

    def _make_sensor_data(self):
        tm = round(time.time(), 2)
        self.data = [tm] + [np.random.randint(0, 2) for _ in self.port_ids]
        self.payload_ = ['"tm":"{0}"'.format(self.data[0])]
        for port_id, randint in zip(self.port_ids, self.data[1:]):
            self.payload_.append('"d{0}":{1}'.format(port_id, randint))
        self.payload = '{{{0}}}'.format(','.join(self.payload_))


class DigitalCounters(object):
    def __init__(self, username, password, host, device_id, port_ids, periods):
        self.port_ids = port_ids
        self.periods = periods
        self.counters = {}
        for i, (port_id, period) in enumerate(zip(port_ids, periods)):
            self.counters[i] = DigitalCounter('Digital_counters', username, password, host, device_id, port_id, period)

    def run(self):
        for counter in self.counters.values():
            counter.start()


class DigitalCounter(Sensor, threading.Thread):
    def __init__(self, name, username, password, host, device_id, port_id, period):
        super(DigitalCounter, self).__init__(name, device_id)
        super(Sensor, self).__init__()
        self.username = username
        self.password = password
        self.host = host
        self.device_id = device_id
        self.port_id = port_id
        self.period = period
        self.header = ['time', 'd{}'.format(port_id)]
        self._init_logfile()
        self.setDaemon(True)

    def _make_sensor_data(self):
        tm = round(time.time(), 2)
        self.data = [tm, np.random.randint(0, 50)]
        self.payload = '{{"tm":"{0}","d{1}":{2}}}'.format(self.data[0], self.port_id, self.data[1])


class DigitalElements(object):
    def __init__(self, username, password, host, device_id, global_period, periods=8*[0]):
        sensor_ids = [i+1 for i, p in enumerate(periods) if p==0]
        counter_ids = list(set(xrange(1, 9)) - set(sensor_ids))
        counter_periods = [p for p in periods if p!=0]
        self.sensors = DigitalSensors('Digital_sensors', username, password, host, device_id, sensor_ids, global_period)
        self.counters = DigitalCounters(username, password, host, device_id, counter_ids, counter_periods)

    def run(self):
        self.sensors.start()
        self.counters.run()


class AnalogSensors(Sensor, threading.Thread):
    def __init__(self, name, username, password, host, device_id, period):
        super(AnalogSensors, self).__init__(name, device_id)
        super(Sensor, self).__init__()
        self.username = username
        self.password = password
        self.host = host
        self.device_id = device_id
        self.period = period
        self.t = 0
        self.dt = 0.1
        self.header = ['time'] + ['a{}'.format(i+1) for i in xrange(8)]
        self._init_logfile()
        self.setDaemon(True)

    def _make_sensor_data(self):
        tm = round(time.time(), 2)
        a1 = round(np.random.rand() + 10 + 10*np.sin(2*np.pi*self.t), 2)
        a2 = round(np.random.rand() + 20 + 20*np.sin(2*np.pi*self.t), 2)
        a3 = round(np.random.rand() + 30 + 30*np.sin(2*np.pi*self.t), 2)
        a4 = round(np.random.rand() + 40 + 40*np.sin(2*np.pi*self.t), 2)
        a5 = round(np.random.rand() + 10 + 10*np.cos(2*np.pi*self.t), 2)
        a6 = round(np.random.rand() + 20 + 20*np.cos(2*np.pi*self.t), 2)
        a7 = round(np.random.rand() + 30 + 30*np.cos(2*np.pi*self.t), 2)
        a8 = round(np.random.rand() + 40 + 40*np.cos(2*np.pi*self.t), 2)
        self.t += self.dt
        self.data = [tm, a1, a2, a3, a4, a5, a6, a7, a8]
        self.payload = '{{"tm":"{0}","a1":{1},"a2":{2},"a3":{3},"a4":{4},"a5":{5},"a6":{6},"a7":{7},"a8":{8}}}'.format(*self.data)


class Device(object):
    def __init__(self, username, password, host, device_id, p_beacon=BEACON_PERIOD, p_env=ENV_PERIOD, p_digi=DIGITAL_SENSOR_PERIOD, p_ana=ANALOG_SENSOR_PERIOD):
        self.username = username
        self.password = password
        self.host = host
        self.device_id = device_id
        self.beacon = Beacon('Beacon', username, password, host, device_id, p_beacon, beacon=device_id)
        self.envinfo = EnvironmentalInformation('EnvInfo', username, password, host, device_id, p_env)
        self.digital_elems = DigitalElements(username, password, host, device_id, global_period=p_digi, periods=DIGITAL_COUNTER_PERIODS)
        self.anasnsrs = AnalogSensors('Analog_sensors', username, password, host, device_id, p_ana)

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
