# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# vim: set foldmethod=marker commentstring=\ \ #\ %s :
#
# Author:    Taishi Matsumura
# Created:   2018-04-18
#
# Copyright (C) 2018 Taishi Matsumura
#
from distutils.core import setup
import py2exe

option = {'bundle_files': 3,
        'compressed': True}

setup(options={'py2exe': option},
        console=['main2.py'],
        zipfile='main2.zip')
