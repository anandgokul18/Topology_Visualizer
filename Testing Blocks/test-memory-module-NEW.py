#!/usr/bin/env python3

#Python in-built Library Imports
import sys
import re
import time

#Python Packages
import pygsheets

#Swat Module Imports
from labLib import findDuts

dut='cd526'

import cliLib

obj = cliLib.CliSession(Host=dut, Username='admin', Password='', Timeout=30)
obj.createCliSession()
obj.cliSend(cmd='enable', raw=True)
temp=obj.cliSend(cmd='show version | json | grep memTotal', raw=True)

#print(temp)

temp_result=str(temp).split('"memTotal": ')
result=temp_result[1].split(',')[0]

#Rounding the value to nearest number
result=int(result)/1000000
result = str(int(round(result, 0)))
#print(result)