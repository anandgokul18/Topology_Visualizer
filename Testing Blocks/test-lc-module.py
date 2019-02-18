#!/usr/bin/env python3

#Python in-built Library Imports
import sys
import re
import time

#Python Packages
import pygsheets

#Swat Module Imports
from labLib import findDuts

dut='tg310'

from initToolLib import connectDevices

class ModuleInfo:
	def getModuleInfo(self, *args):
		'''
        This method returns the information about the modules on a DUT.

        Inputs :  None

        Outputs:  A list containing the names of linecards.
        '''

		# Initialize Variables
		cmd    = 'show module'
		retVal = []


		##ASSUMING SSH ACCESS .ie. API=False
		# Goto Appropriate Prompt Level
		self._enablePrompt()
		output = self._cliSend(cmd)

		# Preparing Output data
		for line in output[1:]:

			# Ignore Empty Lines
			if line: retVal.append(line[0].lower())

		# Return List of Interfaces
		return retVal


a=connectDevices(dut, api=False)
a,=a
temp = a.getModuleInfo()

#print(temp)
varForOnlyLinecards=[value for key, value in temp.items() if 'Linecard' in key or 'Supervisor' in key]
#print(len(varForOnlyLinecards))
i=0
lc_list=[]
for i in range(0,len(varForOnlyLinecards)):
	lc_list.append(varForOnlyLinecards[i]['model'])

print(lc_list)
