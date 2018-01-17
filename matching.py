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
time_stamp = '20171227102729'
begin = '2017-12-27 10:28:00'
end = '2017-12-27 10:47:00'


# load the data downloaded from the server as server_data
headers = ['time'] + ['d{}'.format(i+1) for i in xrange(8)] + ['a{}'.format(i+1) for i in xrange(8)] + ['eiHumi', 'eiLPrs', 'eiTemp', 'seaPrs', 'beacon', 'message', 'dummy']
server_data_raw = pd.read_csv('./receivedata.csv', header=0, names=headers).set_index('time')

for sensor_name in sensor_names:
    # load the data stored by python as local_data
    file_path = './Logs/IFT_ML1-YONEZAWA{:04d}/{}_{}.csv'.format(device_id, sensor_name, time_stamp)
    tmp_data = pd.read_csv(file_path).set_index('time')
    tmp_data = tmp_data.loc[begin:end, :]
    tmp_data = tmp_data.iloc[:, 0:-1]
    local_data = {sensor_name: tmp_data}

    # extract data of the sensor from the server_data
    server_data = {sensor_name: server_data_raw.loc[begin:end, tmp_data.columns].dropna(how='all', axis=0)}

    df = pd.concat([local_data[sensor_name], server_data[sensor_name]], axis=1)
    judge_table = local_data[sensor_name] == server_data[sensor_name]
    result = all(judge_table)
    print judge_table

    okng = 'OK'*result + 'NG'*(not result)
    print '{}: {}'.format(sensor_name, okng)
