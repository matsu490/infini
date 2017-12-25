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
sensor_names = ['Beacon', 'Analog_sensors']
at = '20171225105711'
begin = '2017-12-25 11:56:00'
end = '2017-12-25 11:58:00'


# load the data downloaded from the server as server_data
headers = ['time'] + ['d{}_s'.format(i+1) for i in xrange(8)] + ['a{}_s'.format(i+1) for i in xrange(8)] + ['eiTemp_s', 'eiHumi_s', 'eiLPrs_s', 'seaPrs_s', 'beacon_s', 'message_s', 'dummy_s']
server_data_raw = pd.read_csv('./receivedata.csv', header=0, names=headers).set_index('time')

for sensor_name in sensor_names:
    # load the data stored by python as local_data
    file_path = './Logs/IFT_ML1-YONEZAWA{:04d}/{}_{}.csv'.format(device_id, sensor_name, at)
    tmp_data = pd.read_csv(file_path).set_index('time')
    if sensor_name == 'Beacon':
        tmp_data = tmp_data.loc[begin:end, 'message']
    elif sensor_name == 'Analog_sensors':
        tmp_data = tmp_data.loc[begin:end, 'a1':'a8']
    local_data = {sensor_name: tmp_data}

    # extract data of the sensor from the server_data
    if sensor_name == 'Beacon':
        server_data = {sensor_name: server_data_raw.loc[begin:end, 'beacon_s'].dropna(how='all', axis=0)}
    elif sensor_name == 'Analog_sensors':
        server_data = {sensor_name: server_data_raw.loc[begin:end, 'a1_s':'a8_s'].dropna(how='all', axis=0)}

    df = pd.concat([local_data[sensor_name], server_data[sensor_name]], axis=1)
    judge_table = local_data[sensor_name] == server_data[sensor_name]
    result = bool(np.all(judge_table))

    okng = 'OK'*result + 'NG'*(not result)
    print '{}: {}'.format(sensor_name, okng)
