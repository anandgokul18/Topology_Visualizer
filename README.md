# Bangalore-Systest-RackMap

This repo contains the script made for Arista Networks Bangalore Systest Remote team to visualize the locations of switches and routers in datacenter. This script will get the devices from Arista Internal device Database and populate their location on an Google Sheet.

Apart from visualizing their location on Google Sheet, this script also calculates the distance of cabling required for each user, gives the supervisor and linecard info for modular switches, and also gives the memory info of each device.

The device list must be passed as a dictionary to 'alldevices' variable inside BangaloreRackDeviceList() function and you are good to go...

All proprietary information has been removed and the code can be modified freely by anyone...
