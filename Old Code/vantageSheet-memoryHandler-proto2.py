#!/usr/bin/env python3

#Swat Module Imports
from labLib import findDuts
import cliLib

#Python Module Imports
import json
import re

##Getting all device list
def bangaloreRackDeviceList_New():
	alldevices= findDuts(prefixes=None, chipsets=None, category='all', pool='LabTracker', all=True)
	devices=alldevices.items()
	##print devices

	blrDevices={}
	regex= r"(dm1-rack1(0[3-9]|1[0-8]))"

	for i,data in enumerate(devices):
		if re.match(regex, data[1]['location']):
			blrDevices[data[0]]=[data[1]['location'],data[1]['category'],data[1]['owner'],data[1]['chipsets']]

	return blrDevices


##Getting all memory of the devices
def memoryInfo_New(dut):
	try:
		
		obj = cliLib.CliSession(Host=dut, Username='admin', Password='arastra', Timeout=60)
		obj.createCliSession()
		obj.cliSend(cmd='enable', raw=True)
		temp=obj.cliSend(cmd='show version | json | grep memTotal', raw=True)

		temp_result=str(temp).split('"memTotal": ')
		result=temp_result[1].split(',')[0]

		#Rounding the value to nearest number
		result=int(result)/1000000
		result = str(int(round(result, 0)))
		return result

	except Exception as e:
		#print('Error in getting memory Info for DUT '+dut +':')
		#print(e)
		return 'Unknown'

if __name__== "__main__":

	blrDevices = bangaloreRackDeviceList_New()
	#blrDevices={'fm367':1,'tg310':2}

	memoryofDuts={}

	for dut in blrDevices.keys():
		memoryofDuts[dut]=memoryInfo_New(dut)
		#print(memoryofDuts+'\n\n')

	#print(memoryofDuts)

	#Writing the dictionary to file
	json.dump(memoryofDuts, open("memorylist.txt",'w'))
	#with open('memorylist.txt','w') as data:
	#	data.write(str(memoryofDuts))

