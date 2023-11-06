#!/usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO

import serial
import time
import math
import re
from message import messagefrom message import message


obj = message()
obj.ALERT()