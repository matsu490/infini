# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# vim: set foldmethod=marker commentstring=\ \ #\ %s :
#
# Author:    Taishi Matsumura
# Created:   2017-11-16
#
# Copyright (C) 2017 Taishi Matsumura
#
import numpy as np
import pandas as pd

device_id = 1
sensor_name = 'Analog_sensors'
at = '20171225105711'
begin = '2017-12-25 11:56:00'
end = '2017-12-25 11:58:00'

# load the data stored by python as local_data
file_path = './Logs/IFT_ML1-YONEZAWA{:04d}/{}_{}.csv'.format(device_id, sensor_name, at)
tmp_data = pd.read_csv(file_path).set_index('time')
tmp_data = tmp_data.loc[begin:end, 'a1':'a8']
local_data = {sensor_name: tmp_data}

# load the data downloaded from the server as server_data
headers = ['time'] + ['sd{}'.format(i+1) for i in xrange(8)] + ['sa{}'.format(i+1) for i in xrange(8)] + ['seiTemp', 'seiHumi', 'seiLPrs', 'sseaPrs', 'sbeacon', 'smessage', 'dummy']
server_data_raw = pd.read_csv('./receivedata.csv', header=0, names=headers).set_index('time')
# server_data = {sensor_name: server_data_raw.query('index in @local_data[@sensor_name].index').loc[:, 'sa1':'sa8']}
server_data = {sensor_name: server_data_raw.loc[begin:end, 'sa1':'sa8'].dropna(how='all', axis=0)}

df = pd.concat([local_data[sensor_name], server_data[sensor_name]], axis=1)
print np.logical_and(local_data[sensor_name], server_data[sensor_name])


'''
# Load the .csv file
time.sleep(5)
num = 1
dic = {}
if num == 1:
    csv_name = 'receivedata.csv'
elif num > 1:
    csv_name = 'receivedata ({:d}).csv'.format(num - 1)
csv_path = 'C:/Users/admin/Downloads/{}'.format(csv_name)

if os.path.exists(csv_path):
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        dic['Kenshouki{:04d}'.format(num)] = [csv_name, reader]
else:
    pass

num += 1
'''
