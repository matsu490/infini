# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# vim: set foldmethod=marker commentstring=\ \ #\ %s :
#
# Author:    Taishi Matsumura
# Created:   2017-11-16
#
# Copyright (C) 2017 Taishi Matsumura
#
import pandas as pd

device_id = 1
sensor_names = ['EnvInfo', 'Analog_sensors', 'Digital_sensors', 'Digital_counters', 'Beacon']
sensor_names = ['Analog_sensors']
time_stamp = '20180411113613'
begin = '2018-04-11 11:36:00'
end = '2018-04-11 11:46:00'


# server_data: load the data downloaded from the server
headers = ['time'] + ['d{}'.format(i+1) for i in xrange(8)] + ['a{}'.format(i+1) for i in xrange(8)] + ['eiTemp', 'eiHumi', 'eiLPrs', 'seaPrs', 'beacon', 'message']
server_data_raw = pd.read_csv('./receivedata.csv', header=0, names=headers).set_index('time')

for sensor_name in sensor_names:
    # local_data: load the data stored by python in local
    file_path = './Logs/IFT_ML1-YONEZAWA{:04d}/{}_{}.csv'.format(device_id, sensor_name, time_stamp)
    tmp_data = pd.read_csv(file_path).set_index('time')
    tmp_data = tmp_data.loc[begin:end, :]
    tmp_data = tmp_data.iloc[:, 0:-1]
    local_data = {sensor_name: tmp_data}

    # extract data of the sensor from the server_data
    server_data = {sensor_name: server_data_raw.loc[begin:end, tmp_data.columns].dropna(how='all', axis=0)}

    df = pd.concat([local_data[sensor_name], server_data[sensor_name]], axis=1)
    judge_table = local_data[sensor_name] == server_data[sensor_name]
    result = all(judge_table.all())
    print judge_table

    okng = 'OK'*result + 'NG'*(not result)
    print '{}: {}'.format(sensor_name, okng)
