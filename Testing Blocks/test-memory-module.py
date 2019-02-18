#!/usr/bin/env python3

import pexpect

def memoryInfo(dut):
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

		'''
        child = pexpect.spawn("ssh "+ "admin@"+dut,timeout=30)
        #cmd="show version | grep -i 'Total memory:'"
        cmd1="show version | json | grep memTotal"

        try: #if device is in user mode
            child.expect(">")
            child.sendline(cmd1)
            #Saving the output to duts1
            child.expect(">")
            output= (child.before)
            #print(output)

        except: #if device is in exec mode
            child.expect("#")
            child.sendline(cmd1)
            #Saving the output to duts1
            child.expect("#")
            output= (child.before)
            #print(output)
		'''

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

result=memoryInfo('fu636')
print(result)