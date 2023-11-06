#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import subprocess
import time

# Run script1.py from directory1
subprocess.Popen(['python3', '/home/vuyisa/Documents/CameraTrap.py'])
time.sleep(5)

# Run script2.py from directory2
subprocess.Popen(['python3', '/home/vuyisa/pySX1278/testing.py'])