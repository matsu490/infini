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
import Tkinter as tk
import numpy as np
from params import *


class InitDialog(tk.Frame, object):
    def __init__(self, master=None):
        super(InitDialog, self).__init__(master)
        self.pack()
        self._init_widgets()

    def _init_widgets(self):
        self.bools4analog1 = [tk.BooleanVar() for i in xrange(8)]
        self.checkboxes4analog1 = [tk.Checkbutton(variable=self.bools4analog1[i]) for i in xrange(8)]
        for i in xrange(8):
            self.bools4analog1[i].set(bool(ANALOG_GROUP1[i]))
            self.checkboxes4analog1[i].pack(side='left')

        self.ok_button = tk.Button(
                self,
                text='OK',
                command=self.quit)
        self.ok_button.pack()


class Sensor(object):
    def __init__(self, name, device_id):
        self.sensor_name = name
        self.device_id = device_id
        self.header = []
        self.logfile_path = ''
        self.temp_logfile_path = ''
        self.io_error = False

    def _init_logfile(self):
        self._make_logdir()
        self.logfile_path = './Logs/{}/{}_{}.csv'.format(self.device_id, self.sensor_name, self._timestamp())
        self.temp_logfile_path = os.path.splitext(self.logfile_path)[0] + '.tmp'
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
            if self.io_error:
                pass
            # If the IOError didn't happen previously, make a new templogfile.
            else:
                self._make_logfile(self.temp_logfile_path, self.header + ['is_err'])
            self._write_log(self.temp_logfile_path, line)
            self.io_error = True
        else:
            # If the IOError happend previously, merge and remove the templogfile.
            if self.io_error:
                self._merge_templogfile()
                os.remove(self.temp_logfile_path)
            self.io_error = False

    def _merge_templogfile(self):
        with open(self.logfile_path, 'r') as f:
            log_file = f.readlines()
        with open(self.temp_logfile_path, 'r') as f:
            temp_log = f.readlines()
        log_file[-1:0] = temp_log[1:]
        with open(self.logfile_path, 'w') as f:
            f.writelines(log_file)

    def _make_logfile(self, file_path, line):
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
    def __init__(self, name, username, password, host, device_id, period, check_box):
        super(AnalogSensors, self).__init__(name, device_id)
        super(Sensor, self).__init__()
        self.username = username
        self.password = password
        self.host = host
        self.device_id = device_id
        self.period = period
        self.check_box = check_box
        self.port_ids = [i+1 for i in xrange(len(check_box)) if check_box[i]==1]
        self.header = ['time'] + ['a{}'.format(port_id) for port_id in self.port_ids]
        self.t = 0
        self.dt = 0.1
        self._init_logfile()
        self.setDaemon(True)

    def _make_sensor_data(self):
        tm = round(time.time(), 2)
        waves = [round(np.random.rand() + 10 + 10*np.sin(2*np.pi*self.t), 2),
                 round(np.random.rand() + 20 + 20*np.sin(2*np.pi*self.t), 2),
                 round(np.random.rand() + 30 + 30*np.sin(2*np.pi*self.t), 2),
                 round(np.random.rand() + 40 + 40*np.sin(2*np.pi*self.t), 2),
                 round(np.random.rand() + 10 + 10*np.cos(2*np.pi*self.t), 2),
                 round(np.random.rand() + 20 + 20*np.cos(2*np.pi*self.t), 2),
                 round(np.random.rand() + 30 + 30*np.cos(2*np.pi*self.t), 2),
                 round(np.random.rand() + 40 + 40*np.cos(2*np.pi*self.t), 2)]
        self.data = [tm] + [waves[i-1] for i in self.port_ids]
        self.payload_ = ['"tm":"{0}"'.format(self.data[0])]
        for port_id, wave in zip(self.port_ids, self.data[1:]):
            self.payload_.append('"a{0}":{1}'.format(port_id, wave))
        self.payload = '{{{0}}}'.format(','.join(self.payload_))
        self.t += self.dt


class Device(object):
    def __init__(self, username, password, host, device_id, p_beacon=BEACON_PERIOD, p_env=ENV_PERIOD, p_digi=DIGITAL_SENSOR_PERIOD):
        self.username = username
        self.password = password
        self.host = host
        self.device_id = device_id
        self.beacon = Beacon('Beacon', username, password, host, device_id, p_beacon, beacon=device_id)
        self.envinfo = EnvironmentalInformation('EnvInfo', username, password, host, device_id, p_env)
        self.digital_elems = DigitalElements(username, password, host, device_id, global_period=p_digi, periods=DIGITAL_COUNTER_PERIODS)
        self.anagroup1 = AnalogSensors('Analog_group1', username, password, host, device_id, ANALOG_GROUP1_PERIOD, ANALOG_GROUP1)
        self.anagroup2 = AnalogSensors('Analog_group2', username, password, host, device_id, ANALOG_GROUP2_PERIOD, ANALOG_GROUP2)
        self.anagroup3 = AnalogSensors('Analog_group3', username, password, host, device_id, ANALOG_GROUP3_PERIOD, ANALOG_GROUP3)
        self.anagroup4 = AnalogSensors('Analog_group4', username, password, host, device_id, ANALOG_GROUP4_PERIOD, ANALOG_GROUP4)

    def switch_on(self):
        self.beacon.start()
        self.envinfo.start()
        self.digital_elems.run()
        self.anagroup1.start()
        self.anagroup2.start()
        self.anagroup3.start()
        self.anagroup4.start()


class Devices(object):
    def __init__(self, device_name, n, username, password, host):
        self.device_name = device_name
        self.n = n
        self.username = username
        self.password = password
        self.host = host
        self.devices = {}
        self._init_devices()

    def _init_devices(self):
        if self.n == 1:
            self.devices[1] = Device(self.username, self.password, self.host, self.device_name)
        elif self.n > 1:
            for i in xrange(1, self.n+1):
                device_id = '{0}{1}'.format(self.device_name, '{:04d}'.format(i))
                self.devices[i] = Device(self.username, self.password, self.host, device_id)
        else:
            raise DataRangeError()

    def switch_on(self):
        for i in xrange(1, self.n+1):
            self.devices[i].switch_on()


class DataRangeError(Exception):
    def __str__(self):
        return 'The value is out of range.'


if __name__ == '__main__':
    root = tk.Tk()
    root.title('test')
    root.geometry('400x300')
    app = InitDialog(master=root)
    app.mainloop()
    root.destroy()

    devices = Devices(DEVICE_NAME, N_DEVICE, USERNAME, PASSWORD, HOST)
    devices.switch_on()

    while True:
        c = sys.stdin.read(1)
        if c == 'e':
            sys.exit()
