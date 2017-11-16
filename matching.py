# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# vim: set foldmethod=marker commentstring=\ \ #\ %s :
#
# Author:    Taishi Matsumura
# Created:   2017-11-16
#
# Copyright (C) 2017 Taishi Matsumura
#


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
