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

		ssh_newkey = 'Are you sure you want to continue connecting'

		child = pexpect.spawn("ssh admin@"+dut,timeout=40)
		try:
			ret_val=child.expect([ssh_newkey,"word",">","#"])   #This o/p can be either one of the three cases
		except Exception as e:
			print('Error in getting memory Info for DUT '+dut +':')
			print(e)
			return 'Not known'
			
		if ret_val == 0:
			child.sendline('yes')
			ret_val=child.expect([ssh_newkey,'password:',">"])
		elif ret_val==1:
			child.sendline("arastra")
			child.expect("#")
		elif ret_val==2:
			pass
		elif ret_val==3:
			pass

		child.sendline("enable")
		child.expect("#")
		cmd1="show version | json | grep memTotal"
		child.sendline(cmd1)
		child.expect("#")
		output= (child.before)
		#print(output)

		temp_result=str(output).split('"memTotal": ')
		result=temp_result[1].split(',')[0]

		#Rounding the value to nearest number
		result=int(result)/1000000
		result = str(int(round(result, 0)))
		return result

	except Exception as e:
		print('Error in getting memory Info for DUT '+dut +':')
		print(e)
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

