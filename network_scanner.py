#!/usr/bin/env python

import scapy.all as scapy

# import optparse #Comment for Ptyhon3
import argparse #Uncomment for Python3

def parsing_arguments():
   # parser = optparse.OptionParser()   #Uncomment for Python3
    parser = argparse.ArgumentParser()  #Comment for Ptyhon3
   # parser.add_option("-t","--target",dest="range",help="Specify range to be discover") #Comment for Ptyhon3
    parser.add_argument("-t","--target",dest="range",help="Specify range to be discover") #Uncomment for Python3
    return parser.parse_args()

def scan(ip):

    arp_request = scapy.ARP(pdst=ip)  # CREATING ARP REQUEST OBJECT
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")  # CREATING ETHERNET PACKET OBJECT
    arp_request_broadcast = broadcast/arp_request   # Appending ARP Packet to Ether message
    answered_list = scapy.srp(arp_request_broadcast, timeout=1,verbose=False)[0]  # Capturing ARP Reply
    client_list=[]
    for element in answered_list:
        client_dic={"ip":element[1].psrc,"mac":element[1].hwsrc}
        client_list.append(client_dic)
    return client_list

def print_list(results_list):
    print("IP\t\t\t\tMAC Adress\n--------------------------------------------------")
    for client in results_list:
        print(client["ip"]+"\t\t\t"+client["mac"])

options=parsing_arguments() #Uncomment for Python3
# (options,arguments) = parsing_arguments() #Comment for Python3
scan_result=scan(options.range)
print_list(scan_result)

