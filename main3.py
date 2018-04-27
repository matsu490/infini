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
import paho.mqtt.publish as publish
import Tkinter as tk
import numpy as np
from params import *


class MainDialog(tk.Frame, object):
    def __init__(self, master=None):
        super(MainDialog, self).__init__(master)
        self.pack()
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
        self._stack('Run button', tk.Button(self, text='Run', command=self._cb_run_button))
        self._stack('Stop button', tk.Button(self, text='Stop', command=self._cb_stop_button))

    def _stack(self, name, UI):
        self.UIs[name] = UI
        self.UIs[name].grid(row=len(self.UIs), column=0, sticky=tk.W)

    def _cb_run_button(self):
        print '/////////////////////////////////////////'
        print '///         Run the devices           ///'
        print '/////////////////////////////////////////'

    def _cb_stop_button(self):
        print '/////////////////////////////////////////'
        print '///         Stop the devices          ///'
        print '/////////////////////////////////////////'


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


if __name__ == '__main__':
    root = tk.Tk()
    root.title('test')
    root.geometry('500x400')
    app = MainDialog(master=root)
    app.mainloop()
