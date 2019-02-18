#!/usr/bin/env python3

#Python in-built Library Imports
import sys
import re
import time

#Python Packages
import pygsheets

#Swat Module Imports
from labLib import findDuts



def bangaloreRackDeviceList():
	alldevices= findDuts(prefixes=None, chipsets=None, category='all', pool='LabTracker', all=True)
	devices=alldevices.items()
	##print devices

	blrDevices={}
	regex= r"(dm1-rack1(0[3-9]|1[0-8]))"

	for i,data in enumerate(devices):
		if re.match(regex, data[1]['location']):
			blrDevices[data[0]]=[data[1]['location'],data[1]['category'],data[1]['owner'],data[1]['chipsets']]

	return blrDevices

def clearExcel():
	
	#Clearing previous values. If any fixed device location is changed, modify this sheet
	wks.clear(start='B5', end='B50', fields='*')
	
	wks.clear(start='C9', end='C50', fields='*')
	
	wks.clear(start='D5', end='D50', fields='*')
	wks.clear(start='E5', end='E50', fields='*')
	
	wks.clear(start='F17', end='F38', fields='*')
	
	wks.clear(start='G5', end='G50', fields='*')
	wks.clear(start='H5', end='H50', fields='*')
	wks.clear(start='J5', end='J50', fields='*')

	wks.clear(start='K9', end='K39', fields='*')

	wks.clear(start='L5', end='L50', fields='*')
	wks.clear(start='M5', end='M50', fields='*')
	wks.clear(start='N5', end='N50', fields='*')

	wks.clear(start='O5', end='O39', fields='*')

	wks.clear(start='P5', end='P50', fields='*')
	wks.clear(start='Q5', end='Q50', fields='*')
	wks.clear(start='R5', end='R50', fields='*')

def infraAndLabpatch(cellno,devicename):

	cellid=wks.cell(cellno)
	cellid.unlink()
	cellid.value=devicename
	cellid.color=(0.2901961, 0.5254902, 0.9098039, 0) #Color code for Dark Blue
	cellid.link()
	cellid.update()

def findRowAndColumn(location):
	tempList=location.split('-')

	#To find the excel column
	absolutecolumn=tempList[1].split('rack')
	
	if int(absolutecolumn[1])==103:
		excelColumn='B'
	elif int(absolutecolumn[1])==104:
		excelColumn='C'
	elif int(absolutecolumn[1])==105:
		excelColumn='D'
	elif int(absolutecolumn[1])==106:
		excelColumn='E'
	elif int(absolutecolumn[1])==107:
		excelColumn='F'
	elif int(absolutecolumn[1])==108:
		excelColumn='G'
	elif int(absolutecolumn[1])==109:
		excelColumn='H'
	elif int(absolutecolumn[1])==110:
		excelColumn='J'
	elif int(absolutecolumn[1])==111:
		excelColumn='K'
	elif int(absolutecolumn[1])==112:
		excelColumn='L'
	elif int(absolutecolumn[1])==113:
		excelColumn='M'
	elif int(absolutecolumn[1])==114:
		excelColumn='N'
	elif int(absolutecolumn[1])==115:
		excelColumn='O'
	elif int(absolutecolumn[1])==116:
		excelColumn='P'
	elif int(absolutecolumn[1])==117:
		excelColumn='Q'
	elif int(absolutecolumn[1])==118:
		excelColumn='R'
						
	else:
		excelColumn='S' 

	#To find the excel Row
	absoluterow=tempList[2].split('tb')

	excelRow = 51 - int(absoluterow[1])

	return excelColumn, excelRow, absolutecolumn[1]

def modularwriter(dut, owner, excelColumn,excelRow):
	
	excelLocation=excelColumn+str(excelRow)

	try:
		if 'tg' in dut or 'ph' in dut: #7 RU devices
			excelLocation=excelColumn+str(excelRow)
			wks.cell(excelLocation).value = dut +"\n["+owner+"]"
			for i in range(0,6):
				excelRow=excelRow+1
				excelLocation=excelColumn+str(excelRow)
				wks.cell(excelLocation).value = '...'
				time.sleep(2)
				
		elif 'in' in dut: #8 RU devices
			excelLocation=excelColumn+str(excelRow)
			wks.cell(excelLocation).value = dut +"\n["+owner+"]"
			for i in range(0,7):
				excelRow=excelRow+1
				excelLocation=excelColumn+str(excelRow)
				wks.cell(excelLocation).value = '...'
				time.sleep(2)

		elif 'yo' in dut or 'bh' in dut: #13 RU devices
			excelLocation=excelColumn+str(excelRow)
			wks.cell(excelLocation).value = dut +"\n["+owner+"]"
			for i in range(0,12):
				excelRow=excelRow+1
				excelLocation=excelColumn+str(excelRow)
				wks.cell(excelLocation).value = '...'
				time.sleep(2)

		else: #2 RU devices
			excelLocation=excelColumn+str(excelRow)
			wks.cell(excelLocation).value = dut +"\n["+owner+"]"
			for i in range(0,1):
				excelRow=excelRow+1
				excelLocation=excelColumn+str(excelRow)
				wks.cell(excelLocation).value = '"""'
				time.sleep(2)

	except Exception as e:
		print("[ERROR] One modular chassis: "+ dut + " has incorrect rack info in labtracker. Because of this, it is overlapping with another device. Fix it in labtracker first to proceed. \n Exiting...")
		print('[FURTHER STEPS] Always modular chassis should be represented with the lowest RU/tb number in rdam')
		print(e)
		sys.exit(1)

def offendingUsers(userRowDict):

	wks2=sh.worksheet_by_title("Vantage- FarAway Users")

	wks2.clear(start='A2', end='A100', fields='*')
	wks2.clear(start='B2', end='B100', fields='*')
	wks2.clear(start='C2', end='C100', fields='*')

	m=2

	#This is to prevent key error since there are no devices in rack84 (ixia rack)
	userRowDict['84']=[]
	
	i=103
	while(i!=110):
		j=i+3
		while(j!=119):
			try:
				if list(set(userRowDict[str(i)]) & (set(userRowDict[str(j)])))!=None:
					names=list(set(userRowDict[str(i)]) & (set(userRowDict[str(j)])))
					for name in names:
						if 'free' not in name:
							name_location='A'+str(m)
							start_rack_location='B'+str(m)
							end_rack_location='C'+str(m)
							m+=1
							wks2.cell(name_location).value = name
							time.sleep(2)
							wks2.cell(start_rack_location).value = str(i)
							time.sleep(2)
							wks2.cell(end_rack_location).value = str(j)
							time.sleep(2)
			except:
				pass
			j+=1
		i+=1



if __name__== "__main__":

	#Create a Google Sheets API Key and then use that Key below
	gc = pygsheets.authorize(service_file='/home/anandgokul/BangaloreRackSheet-Script/mypkey.json')
	#gc = pygsheets.authorize(service_file='mypkey.json')
        #Also, we need to change the quota to 1000 from the default of 100 per user

	#Change the Sheet URL to Arista Domain URL later
	sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1IK-SBOskJnK4aoUI1MohT-QUpTVnS8FCbyKTMsMHLgQ/edit#gid=0")

	#Open Worksheet by name
	wks = sh.worksheet_by_title("Vantage Map")


	blrDevices = bangaloreRackDeviceList()
	##print blrDevices
	##blrDevices = {'fu514': ['r160-rack89-tb19', 'fixed', 'viswanath', ['Xp80']], 'in310': ['r160-rack89-tb1', 'chassis', 'praneeth', ['Trident2', 'Tomahawk']]}


	#To delete all previous values( this is in case the old location is not overwritten)
	clearExcel()

	#Marking Infrastructure and labpath pool Devices
	infraAndLabpatch('J9','Spine42-Infra')
	infraAndLabpatch('J10','Spine41-Infra')
	infraAndLabpatch('C42','tst-cva-04')
	infraAndLabpatch('C41','tst-srv-18')
	infraAndLabpatch('C40','tst-srv-17')
	infraAndLabpatch('C39','tst-srv-16')
	infraAndLabpatch('C38','tst-esx-59')
	infraAndLabpatch('C37','tst-esx-58')
	infraAndLabpatch('C36','tst-cva-05')
	infraAndLabpatch('C35','tst-cva-06')

	dictForOffendingUsers={}

	for dut in blrDevices.keys():
		(excelColumn, excelRow, actualRU)=findRowAndColumn(blrDevices[dut][0])
		##print excelColumn, excelRow
				
		#Populating a dictionary of users in each row
		key = actualRU
		dictForOffendingUsers.setdefault(key, [])
		dictForOffendingUsers[key].append(blrDevices[dut][2])
		
		#Handling modular and 2RU devices
		if any(s in dut for s in ('tg', 'ph', 'in','yo','bh','gd','ol','al','wa','nv','wp')):
			modularwriter(dut, blrDevices[dut][2], excelColumn,excelRow)

		else:
			#Pushing the DUT name and Owner Info note to Sheet
			excelLocation=excelColumn+str(excelRow)
			aliasForCell=wks.cell(excelLocation)
			aliasForCell.unlink()
			aliasForCell.value=dut + "\n[" + blrDevices[dut][2] + "]"
			##noteForCell="Owner: "+ blrDevices[dut][2] +"\n" +"Chipset: " + str(blrDevices[dut][3])
			##aliasForCell.note=noteForCell
			aliasForCell.link()
			aliasForCell.update()

			time.sleep(3)
			
	#Updating the Document with the last Updated Time
	wks.clear(start='B63', end='B63', fields='*')
	currenttime=time.ctime()
	wks.cell('B63').set_text_format('bold', True).value = currenttime

	#Finding the users who have devices more than 2 rack away
	offendingUsers(dictForOffendingUsers)
      
	#Adding a print statement so that cron job email will tell so
	print("Completed Successfully- Success rate 100%")
