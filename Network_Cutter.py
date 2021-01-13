#!/usr/bin/env python

#This Script needs to be used along an ARP Spoofer


import subprocess



def chain_creation():


    subprocess.call("sudo iptables -I FORWARD -j NFQUEUE --queue-num 0",shell=True)

def chain_delete():

    subprocess.call("sudo iptables --flush",shell=True)

n=0
while n==0:
    try:
        chain_creation()
    except KeyboardInterrupt:
        print("CTRL C Detected")
        print("Restarting Internet Connection...")
        chain_delete()
        n=1
             

