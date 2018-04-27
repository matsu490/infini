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


class MainDialog(tk.Frame, object):
    def __init__(self, master=None):
        super(MainDialog, self).__init__(master)
        self.pack()
        self.devices = []
        self.UIs = {}
        self._init_widgets()

    def _init_widgets(self):
        self._stack('User name', EditboxFrame(self, USERNAME, 'User name', ''))
        self._stack('Password', EditboxFrame(self, PASSWORD, 'Password', ''))
        self._stack('Host', EditboxFrame(self, HOST, 'Host', ''))
        self._stack('Client ID', EditboxFrame(self, CLIENT_ID, 'Client ID', ''))
        self._stack('QoS', SpinboxFrame(self, QOS, 'QoS', '0, 1, or 2', min=0, max=2, inc=1))
        self._stack('# of devices', SpinboxFrame(self, N_DEVICE, '# of devices', '', min=1))
        self._stack('Device name', EditboxFrame(self, DEVICE_NAME, 'Device name', ''))
        self._stack('Beacon period', SpinboxFrame(self, BEACON_PERIOD, 'Beacon period', 'sec'))
        self._stack('Environment period', SpinboxFrame(self, ENV_PERIOD, 'Environment period', 'sec'))
        self._stack('Digital sensor period', SpinboxFrame(self, DIGITAL_SENSOR_PERIOD, 'Digital sensor period', 'sec'))
        self._stack('Digital counter periods', DigitalCounterFrame(master=self))
        self._stack('Analog group1', AnalogGroupFrame(num=1, master=self))
        self._stack('Analog group2', AnalogGroupFrame(num=2, master=self))
        self._stack('Analog group3', AnalogGroupFrame(num=3, master=self))
        self._stack('Analog group4', AnalogGroupFrame(num=4, master=self))
        self._stack('Run button', tk.Button(self, text='Run', command=self._cb_run_button))
        self._stack('Stop button', tk.Button(self, text='Stop', command=self._cb_stop_button))

    def _stack(self, name, UI):
        self.UIs[name] = UI
        self.UIs[name].grid(row=len(self.UIs), column=0, sticky=tk.W)

    def _cb_run_button(self):
        print '/////////////////////////////////////////'
        print '///         Run the devices           ///'
        print '/////////////////////////////////////////'
        self._reset_global_vars()
        self._print_global_vars()
        self.main()

    def main(self):
        if N_DEVICE == 1:
            self.devices.append(Device(USERNAME, PASSWORD, HOST, DEVICE_NAME))
            self.devices[-1].switch_on()
        elif N_DEVICE > 1:
            for i in xrange(1, N_DEVICE + 1):
                device_id = '{0}{1}'.format(DEVICE_NAME, '{:04d}'.format(i))
                self.devices.append(Device(USERNAME, PASSWORD, HOST, device_id))
                self.devices[-1].switch_on()
        else:
            raise DataRangeError()

    def _cb_stop_button(self):
        print '/////////////////////////////////////////'
        print '///         Stop the devices          ///'
        print '/////////////////////////////////////////'
        for device in self.devices:
            device.switch_off()

    def _reset_global_vars(self):
        global \
            USERNAME,  \
            PASSWORD,  \
            HOST,  \
            CLIENT_ID,  \
            QOS,  \
            N_DEVICE,  \
            DEVICE_NAME,  \
            BEACON_PERIOD,  \
            ENV_PERIOD,  \
            DIGITAL_SENSOR_PERIOD,  \
            DIGITAL_COUNTER_PERIODS,  \
            ANALOG_GROUP1_PERIOD,  \
            ANALOG_GROUP2_PERIOD,  \
            ANALOG_GROUP3_PERIOD,  \
            ANALOG_GROUP4_PERIOD,  \
            ANALOG_GROUP1,  \
            ANALOG_GROUP2,  \
            ANALOG_GROUP3,  \
            ANALOG_GROUP4

        USERNAME = self.UIs['User name'].get()
        PASSWORD = self.UIs['Password'].get()
        HOST = self.UIs['Host'].get()
        CLIENT_ID = self.UIs['Client ID'].get()
        QOS = int(self.UIs['QoS'].get())
        N_DEVICE = int(self.UIs['# of devices'].get())
        DEVICE_NAME = self.UIs['Device name'].get()
        BEACON_PERIOD = int(self.UIs['Beacon period'].get())
        ENV_PERIOD = int(self.UIs['Environment period'].get())
        DIGITAL_SENSOR_PERIOD = int(self.UIs['Digital sensor period'].get())
        DIGITAL_COUNTER_PERIODS = [int(p.get()) for p in self.UIs['Digital counter periods'].spinboxes]
        ANALOG_GROUP1_PERIOD = int(self.UIs['Analog group1'].period.get())
        ANALOG_GROUP2_PERIOD = int(self.UIs['Analog group2'].period.get())
        ANALOG_GROUP3_PERIOD = int(self.UIs['Analog group3'].period.get())
        ANALOG_GROUP4_PERIOD = int(self.UIs['Analog group4'].period.get())
        ANALOG_GROUP1 = [boolean_var.get()
            for boolean_var in self.UIs['Analog group1'].bools4analog1]
        ANALOG_GROUP2 = [boolean_var.get()
            for boolean_var in self.UIs['Analog group2'].bools4analog1]
        ANALOG_GROUP3 = [boolean_var.get()
            for boolean_var in self.UIs['Analog group3'].bools4analog1]
        ANALOG_GROUP4 = [boolean_var.get()
            for boolean_var in self.UIs['Analog group4'].bools4analog1]

    def _print_global_vars(self):
        print 'USERNAME: {}'.format(USERNAME)
        print 'PASSWORD: {}'.format(PASSWORD)
        print 'HOST: {}'.format(HOST)
        print 'CLIENT_ID: {}'.format(CLIENT_ID)
        print 'QOS: {}'.format(QOS)
        print 'N_DEVICE: {}'.format(N_DEVICE)
        print 'DEVICE_NAME: {}'.format(DEVICE_NAME)
        print 'BEACON_PERIOD: {}'.format(BEACON_PERIOD)
        print 'ENV_PERIOD: {}'.format(ENV_PERIOD)
        print 'DIGITAL_SENSOR_PERIOD: {}'.format(DIGITAL_SENSOR_PERIOD)
        print 'DIGITAL_COUNTER_PERIODS: {}'.format(DIGITAL_COUNTER_PERIODS)
        print 'ANALOG_GROUP1_PERIOD: {}'.format(ANALOG_GROUP1_PERIOD)
        print 'ANALOG_GROUP2_PERIOD: {}'.format(ANALOG_GROUP2_PERIOD)
        print 'ANALOG_GROUP3_PERIOD: {}'.format(ANALOG_GROUP3_PERIOD)
        print 'ANALOG_GROUP4_PERIOD: {}'.format(ANALOG_GROUP4_PERIOD)
        print 'ANALOG_GROUP1: {}'.format(ANALOG_GROUP1)
        print 'ANALOG_GROUP2: {}'.format(ANALOG_GROUP2)
        print 'ANALOG_GROUP3: {}'.format(ANALOG_GROUP3)
        print 'ANALOG_GROUP4: {}'.format(ANALOG_GROUP4)


class SpinboxFrame(tk.Frame, object):
    def __init__(self, master, default_value, str1, str2, min=0, max=900, inc=5):
        super(SpinboxFrame, self).__init__(master)
        self.default_value = default_value
        self.str1 = str1
        self.str2 = str2
        self._init_widgets(min, max, inc)

    def _init_widgets(self, min, max, inc):
        self.label1 = tk.Label(self, text=self.str1)
        self.label2 = tk.Label(self, text=self.str2)
        self.spinbox = tk.Spinbox(self, from_=min, to=max, increment=inc, width=5)
        self.spinbox.delete(0, 'end')
        self.spinbox.insert(0, self.default_value)
        self.label1.pack(side='left')
        self.spinbox.pack(side='left')
        self.label2.pack(side='left')

    def get(self):
        return self.spinbox.get()


class EditboxFrame(tk.Frame, object):
    def __init__(self, master, default_value, str1, str2):
        super(EditboxFrame, self).__init__(master)
        self.default_value = default_value
        self.str1 = str1
        self.str2 = str2
        self._init_widgets()

    def _init_widgets(self):
        self.label1 = tk.Label(self, text=self.str1)
        self.label2 = tk.Label(self, text=self.str2)
        self.editbox = tk.Entry(self)
        self.editbox.insert(tk.END, self.default_value)
        self.label1.pack(side='left')
        self.editbox.pack(side='left')
        self.label2.pack(side='left')

    def get(self):
        return self.editbox.get()


class DigitalCounterFrame(tk.Frame, object):
    def __init__(self, master=None):
        super(DigitalCounterFrame, self).__init__(master)
        self.label = 0
        self.spinboxes = []
        self._init_widgets()

    def _init_widgets(self):
        self._init_label()
        self._init_spinboxes()

    def _init_label(self):
        self.label = tk.Label(self, text='Digital counter periods')
        self.label.pack(side='left')

    def _init_spinboxes(self):
        for i, p in enumerate(DIGITAL_COUNTER_PERIODS):
            self.spinboxes.append(tk.Spinbox(self, from_=0, to=900, increment=5, width=5))
            self.spinboxes[-1].delete(0, 'end')
            self.spinboxes[-1].insert(0, p)
            self.spinboxes[-1].pack(side='left')


class AnalogGroupFrame(tk.Frame, object):
    def __init__(self, num, master=None):
        super(AnalogGroupFrame, self).__init__(master)
        self.num = num
        self._init_widgets()

    def _init_widgets(self):
        self.label = tk.Label(self, text='Analog group {}'.format(self.num))
        self.period = tk.Spinbox(self, from_=0, to=900, increment=5, width=5)
        self.period.delete(0, 'end')
        self.period.insert(0, eval('ANALOG_GROUP{}_PERIOD'.format(self.num)))
        self.label.pack(side='left')
        self.period.pack(side='left')

        self.bools4analog1 = [tk.BooleanVar(self) for i in xrange(8)]
        self.checkboxes4analog1 = [tk.Checkbutton(self, variable=self.bools4analog1[i]) for i in xrange(8)]
        for i in xrange(8):
            self.bools4analog1[i].set(bool(eval('ANALOG_GROUP{}[i]'.format(self.num, self.num))))
            self.checkboxes4analog1[i].pack(side='left')


class Sensor(threading.Thread):
    def __init__(self, name, device_id):
        super(Sensor, self).__init__()
        self.sensor_name = name
        self.device_id = device_id
        self.header = []
        self.logfile_path = ''
        self.temp_logfile_path = ''
        self.io_error = False
        self.setDaemon(True)
        self.stop_event = threading.Event()

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
        while not self.stop_event.is_set():
            self._make_sensor_data()
            self._send_sensor_data()
            time.sleep(self.period)

    def stop(self):
        self.stop_event.set()

    def _make_sensor_data(self):
        pass

    def _send_sensor_data(self):
        try:
            publish.single(topic='{}/{}'.format(self.password, self.device_id),
                    payload=self.payload, hostname=self.host,
                    client_id=CLIENT_ID, qos=QOS,
                    auth={'username': self.username, 'password': self.password})
            self._logging(0)
            print '{}: {}\n'.format(self.sensor_name, self.payload)
        except:
            self._logging(1)
            print '{}: The payload was not send.'.format(self.sensor_name)


class Beacon(Sensor):
    def __init__(self, name, username, password, host, device_id, period, beacon):
        super(Beacon, self).__init__(name, device_id)
        self.username = username
        self.password = password
        self.host = host
        self.device_id = device_id
        self.period = period
        self.beacon = beacon
        self.header = ['time', 'beacon']
        self._init_logfile()

    def _make_sensor_data(self):
        tm = round(time.time(), 2)
        self.data = [tm, self.beacon]
        self.payload = '{{"tm":"{0}","Beacon":"{1}"}}'.format(*self.data)


class EnvironmentalInformation(Sensor):
    def __init__(self, name, username, password, host, device_id, period):
        super(EnvironmentalInformation, self).__init__(name, device_id)
        self.username = username
        self.password = password
        self.host = host
        self.device_id = device_id
        self.period = period
        self.t = 0
        self.dt = 0.1
        self.header = ['time', 'eiTemp', 'eiHumi', 'eiLPrs', 'seaPrs']
        self._init_logfile()

    def _make_sensor_data(self):
        tm = round(time.time(), 2)
        eiTemp = round(np.random.rand() + 20   +  10*np.sin(2*np.pi*self.t), 2)
        eiHumi = round(np.random.rand() + 50   +  30*np.sin(2*np.pi*self.t), 2)
        eiLPrs = round(np.random.rand() + 900  + 100*np.sin(2*np.pi*self.t), 2)
        seaPrs = round(np.random.rand() + 1000 + 100*np.sin(2*np.pi*self.t), 2)
        self.t += self.dt
        self.data = [tm, eiTemp, eiHumi, eiLPrs, seaPrs]
        self.payload = '{{"tm":"{0}","eiTemp":{1},"eiHumi":{2},"eiLPrs":{3},"seaPrs":{4}}}'.format(*self.data)


class DigitalSensors(Sensor):
    def __init__(self, name, username, password, host, device_id, port_ids, period):
        super(DigitalSensors, self).__init__(name, device_id)
        self.username = username
        self.password = password
        self.host = host
        self.device_id = device_id
        self.port_ids = port_ids
        self.period = period
        self.header = ['time'] + ['d{}'.format(port_id) for port_id in port_ids]
        self._init_logfile()

    def _make_sensor_data(self):
        tm = round(time.time(), 2)
        self.data = [tm] + [np.random.randint(0, 2) for _ in self.port_ids]
        self.payload_ = ['"tm":"{0}"'.format(self.data[0])]
        for port_id, randint in zip(self.port_ids, self.data[1:]):
            self.payload_.append('"d{0}":{1}'.format(port_id, randint))
        self.payload = '{{{0}}}'.format(','.join(self.payload_))


class DigitalCounter(Sensor):
    def __init__(self, name, username, password, host, device_id, port_id, period):
        super(DigitalCounter, self).__init__(name, device_id)
        self.username = username
        self.password = password
        self.host = host
        self.device_id = device_id
        self.port_id = port_id
        self.period = period
        self.header = ['time', 'd{}'.format(port_id)]
        self._init_logfile()

    def _make_sensor_data(self):
        tm = round(time.time(), 2)
        self.data = [tm, np.random.randint(0, 50)]
        self.payload = '{{"tm":"{0}","d{1}":{2}}}'.format(self.data[0], self.port_id, self.data[1])


class AnalogSensors(Sensor):
    def __init__(self, name, username, password, host, device_id, period, check_box):
        super(AnalogSensors, self).__init__(name, device_id)
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
    def __init__(self, username, password, host, device_id):
        self.username = username
        self.password = password
        self.host = host
        self.device_id = device_id
        self.sensors = {
            'beacon': Beacon('Beacon', username, password, host, device_id, BEACON_PERIOD, beacon=device_id),
            'envinfo': EnvironmentalInformation('EnvInfo', username, password, host, device_id, ENV_PERIOD),
            'anagroup1': AnalogSensors('Analog_group1', username, password, host, device_id, ANALOG_GROUP1_PERIOD, ANALOG_GROUP1),
            'anagroup2': AnalogSensors('Analog_group2', username, password, host, device_id, ANALOG_GROUP2_PERIOD, ANALOG_GROUP2),
            'anagroup3': AnalogSensors('Analog_group3', username, password, host, device_id, ANALOG_GROUP3_PERIOD, ANALOG_GROUP3),
            'anagroup4': AnalogSensors('Analog_group4', username, password, host, device_id, ANALOG_GROUP4_PERIOD, ANALOG_GROUP4)}
        sensor_ids = [i+1 for i, p in enumerate(DIGITAL_COUNTER_PERIODS) if p==0]
        counter_ids = list(set(xrange(1, 9)) - set(sensor_ids))
        counter_periods = [p for p in DIGITAL_COUNTER_PERIODS if p!=0]
        self.sensors['digi_snsrs'] = DigitalSensors('Digital_sensors', username, password, host, device_id, sensor_ids, DIGITAL_SENSOR_PERIOD)
        for i, (counter_id, counter_period) in enumerate(zip(counter_ids, counter_periods)):
            self.sensors['digi_cntr{}'.format(i)] = DigitalCounter('Digital_counters', username, password, host, device_id, counter_id, counter_period)

    def switch_on(self):
        for sensor in self.sensors.values():
            sensor.start()

    def switch_off(self):
        for sensor in self.sensors.values():
            sensor.stop()


class DataRangeError(Exception):
    def __str__(self):
        return 'The value is out of range.'


if __name__ == '__main__':
    root = tk.Tk()
    root.title('test')
    root.geometry('500x400')
    app = MainDialog(master=root)
    app.mainloop()
    root.destroy()
