#!/usr/bin/env python
import subprocess
import optparse
import re
#Function definitions
def change_mac(interface,new_mac):
	subprocess.call(["sudo","ifconfig",interface,"down"])
	subprocess.call(["sudo","ifconfig",interface,"hw","ether",new_mac])
	subprocess.call(["sudo","ifconfig",interface,"up"])

def arping():
	subprocess.call("sudo arping -s "+new_mac+" -p 10.0.2.1 > /dev/null 2>&1 &",shell=True)

def parsing_arguments():
	parser = optparse.OptionParser()
	parser.add_option("-i","--interface",dest="interface",help="Interface to change its MAC address")
	parser.add_option("-m","--mac",dest="new_mac",help="New Mac Address")
	return parser.parse_args()
def mac_reader(interface):
	ifconfig_result=subprocess.check_output(["sudo","ifconfig",interface])
	mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",ifconfig_result) #Only works in Python2
	if mac_address_search_result:
		return (mac_address_search_result.group(0))
	else:
		print("[-] Could not read MAC Address")
def success_checker(interface,new_mac):
	
	
	if mac_reader(interface) == new_mac:
		print("[+] Success in changing MAC Address")
	else:
		print("[-] Could not set Given Mac Address")
	
		

(options,arguments)=parsing_arguments()

if not options.interface or not options.new_mac:
	print("[+] You didnt enter all the values required")
	decision = str(input("What do you want to do? 1)Set my Original Mac 2)Set a new one: "))

	if decision=='2':
		interface=str(input("Set new interface: "))
		new_mac=str(input("Set new Mac: "))
		new_mac_list=list(new_mac.split(":"))
		new=int(new_mac_list[0])
	elif decision=='1':
		new_mac='00:11:22:33:44:55'
		interface ='eth0'
		new=0
	else:
		pass
elif options.new_mac=="permanent":
	new_mac='00:11:22:33:44:55'
	interface ='eth0'
	new=0
else:
	interface=str(options.interface)
	new_mac=str(options.new_mac)
	new_mac_list=list(new_mac.split(":"))
	new=int(new_mac_list[0])
while(new%2==1 & new!=0):
	new_mac=str(input("Pick another Mac Adress: "))
	new_mac_list=list(new_mac.split(":"))
	new=int(new_mac_list[0])

print("Your last Mac was: "+str(mac_reader(interface)))

print("[+] Setting Mac address for " + interface +" to "+new_mac)
change_mac(interface,new_mac)
success_checker(interface,new_mac)
arping()



