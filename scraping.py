# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# vim: set foldmethod=marker commentstring=\ \ #\ %s :
#
# Author:    Taishi Matsumura
# Created:   2017-11-10
#
# Copyright (C) 2017 Taishi Matsumura
#
import bs4
import requests
import selenium.webdriver
import time
import csv
import os.path
from params import *

driver = selenium.webdriver.Chrome('./chromedriver.exe')
# driver = selenium.webdriver.Firefox('.')
driver.get(url)
driver.maximize_window()
uid = driver.find_element_by_name('login_id')
pw = driver.find_element_by_name('password')
uid.send_keys(user_name)
pw.send_keys(password)
# Click the login button
driver.find_element_by_xpath('//*[@id="LoginPanel"]/form/input[3]').click()

driver.get('https://m-linker.infinitec.co.jp/MobileGates2/ReceivedataView')
time.sleep(5)
# Expand the tree for devices
driver.find_element_by_xpath('//*[@id="treeView"]/ul/li[2]/span[2]').click()

# Select a device
driver.find_element_by_xpath('//*[@id="treeView"]/ul/li[4]').click()

# Select the list tab
driver.find_element_by_xpath('//*[@id="listfieldseltab"]').click()

# Check the box for message
driver.find_element_by_xpath('//*[@id="list_checkbox_msg"]/td[1]/input').click()

# Output a .csv file of the table data
elements = driver.find_element_by_id('datePeriod')
select_elements = selenium.webdriver.support.ui.Select(elements)
select_elements.select_by_index(8)
# Specify the period to show
driver.find_element_by_id('startDateValue').clear()
driver.find_element_by_id('endDateValue').clear()
driver.find_element_by_id('startDateValue').send_keys('2017-11-14 10:30')
driver.find_element_by_id('endDateValue').send_keys('2017-11-14 10:35')
driver.find_element_by_name('recievedata').click()
# Download the .csv file
time.sleep(5)
driver.find_element_by_xpath('//*[@id="dataExport"]').click()
