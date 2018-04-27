# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# vim: set foldmethod=marker commentstring=\ \ #\ %s :
#
# Author:    Taishi Matsumura
# Created:   2018-04-27
#
# Copyright (C) 2018 Taishi Matsumura
#
import os
import time
import paho.mqtt.publish as publish
import Tkinter as tk
import numpy as np
from params import *


class MainDialog(tk.Frame, object):
    def __init__(self, master=None):
        super(MainDialog, self).__init__(master)
        self.pack()
        self.forever_flag = False
        self.UIs = {}
        self._init_widgets()

    def _init_widgets(self):
        self._stack('Host', EditboxFrame(self, HOST, 'Host', ''))
        self._stack('Client ID', EditboxFrame(self, CLIENT_ID, 'Client ID', ''))
        self._stack('User name', EditboxFrame(self, USERNAME, 'User name', ''))
        self._stack('Password', EditboxFrame(self, PASSWORD, 'Password', ''))
        self._stack('QoS', SpinboxFrame(self, QOS, 'QoS', '0, 1, or 2', min=0, max=2, inc=1))
        self._stack('Device name', EditboxFrame(self, DEVICE_NAME, 'Device name', ''))
        self._stack('Recipient', EditboxFrame(self, 'msg', 'Recipient', ''))
        self._stack('Data', EditboxFrame(self, '', 'Data', ''))
        self._stack('Publish button', tk.Button(self, text='Publish (once)', command=self._cb_publish_button))
        self._stack('Run button', tk.Button(self, text='Publish (forever)', command=self._cb_run_button))
        self._stack('Stop button', tk.Button(self, text='Stop', command=self._cb_stop_button))
        self.UIs['Run button'].configure(state=tk.NORMAL)
        self.UIs['Stop button'].configure(state=tk.DISABLED)

    def _stack(self, name, UI):
        self.UIs[name] = UI
        self.UIs[name].grid(row=len(self.UIs), column=0, sticky=tk.W)

    def _cb_publish_button(self):
        print
        print '/////////////////////////////////////////'
        print '///          Publish (once)           ///'
        print '/////////////////////////////////////////'
        payload = '{{"tm":"{0}","{1}":"{2}"}}'.format(
                round(time.time(), 2),
                self.UIs['Recipient'].get(),
                self.UIs['Data'].get())
        publisher = Publisher(
                self.UIs['Host'].get(),
                self.UIs['Client ID'].get(),
                self.UIs['User name'].get(),
                self.UIs['Password'].get(),
                self.UIs['QoS'].get(),
                self.UIs['Device name'].get())
        publisher.publish_once(payload)

    def _cb_run_button(self):
        print
        print '/////////////////////////////////////////'
        print '///        Publish (forever)          ///'
        print '/////////////////////////////////////////'
        self.forever_flag = True
        self._publish_forever()
        self.UIs['Run button'].configure(state=tk.DISABLED)
        self.UIs['Stop button'].configure(state=tk.NORMAL)

    def _publish_forever(self):
        publisher = Publisher(
                self.UIs['Host'].get(),
                self.UIs['Client ID'].get(),
                self.UIs['User name'].get(),
                self.UIs['Password'].get(),
                self.UIs['QoS'].get(),
                self.UIs['Device name'].get())
        payload = '{{"tm":"{0}","{1}":"{2}"}}'.format(
                round(time.time(), 2),
                self.UIs['Recipient'].get(),
                self.UIs['Data'].get())
        publisher.publish_once(payload)
        if self.forever_flag:
            self.after(1000, self._publish_forever)

    def _cb_stop_button(self):
        print
        print '/////////////////////////////////////////'
        print '///         Stop the devices          ///'
        print '/////////////////////////////////////////'
        self.forever_flag = False
        self.UIs['Run button'].configure(state=tk.NORMAL)
        self.UIs['Stop button'].configure(state=tk.DISABLED)


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
        return int(self.spinbox.get())


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


class Publisher(object):
    def __init__(self, host, client_id, username, password, qos, device_id):
        self.host = host
        self.client_id = client_id
        self.username = username
        self.password = password
        self.qos = qos
        self.device_id = device_id

    def publish_once(self, payload):
        try:
            publish.single(
                    topic='{}/{}'.format(self.password, self.device_id),
                    payload=payload, hostname=self.host,
                    client_id=self.client_id, qos=self.qos,
                    auth={'username': self.username, 'password': self.password})
            print payload
        except:
            print 'The payload was not sent.'


if __name__ == '__main__':
    root = tk.Tk()
    root.title('test')
    root.geometry('500x400')
    app = MainDialog(master=root)
    app.mainloop()
