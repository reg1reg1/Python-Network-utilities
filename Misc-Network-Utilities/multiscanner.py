import sys
import getopt
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
import queue
import threading
import time

'''
Multiscanner written in python2
* Performs UDP scan
* Performs TCP scans
* Does OS fingerprinting
* Takes user input for Host Ip address, and the start and end ports
* For more information, see usage

Written in python 2
'''
fileName=""
target="0.0.0.0"
start=0
end=65536
def UDPScan(ports):
	global fileName
	global start
	global end
	global target
	print("Initiating UDP scan on IP %s with ports %s to %s" % (target,start,end))
	for port in ports:
		pkt = sr1(IP(dst=target)/UDP(sport=port, dport=port), timeout=2, verbose=0)
		if pkt == None:
			fileName.write("Port: "+str(port)+" \\UDP : Open or Dropped\n")
			print(port,"open|filtered")
		else:
			if pkt.haslayer(ICMP):
				print(port,"closed")
			elif pkt.haslayer(UDP):
				print(port,"open|filtered")
				fileName.write("Port: "+str(port)+" \\UDP : Open\n")
			else:
				print(port,"cannot be determined")
				fileName.write("Port: "+str(port)+ " \\UDP : Unknown\n")

def OSFingerPrinting():
	global target
	global fileName
	packet=IP(dst=target)/ICMP()
	ans= sr1(packet,timeout=2,verbose=0)
	if ans==None:
		print("No - response try with p0f module of scapy")
	elif IP in ans:
		if ans.getlayer(IP).ttl<=64:
			fileName.write("-------------------------OS Fingerprint: Linux-------------------------")
			print("Operating System Flavor: Linux")
		else:
			fileName.write("-------------------------OS Fingerprint: Windows-------------------------")
			print("Operating System Flavor: Windows")

class ScannerThread(threading.Thread):
	def __init__(self,queue,tid):
		threading.Thread.__init__(self)
		self.tid=tid
		self.queue=queue

	def run(self):
		global target
		global fileName
		total_ports=0
		ipaddress=sys.argv[1]
		while True:
			try:
				#print(self.queue.qsize())

				#self.queue.get
				#Fetches an unfinished task from the queue
				#if queue is empty it can wait to get the queue filled
				#timeout in case we do not want to wait
				#Note that this action also removes the item from queue
				port = self.queue.get(timeout=1)
			except queue.Empty:
				#print("Queue is empty, thread-",self.tid," exiting......")
				return
			response=sr1(IP(dst=target)/TCP(dport=port,flags="S"),verbose=False,timeout=5)
			if response:
				if response[TCP].flags==18:
					fileName.write("Port: "+str(port)+" \\TCP : Open\n")
					print("Found port "+str(port)+" to be open")
				else:
					pass
					#print("Thread-",self.tid," found port ",port,"to be closed")
			self.queue.task_done()
			total_ports+=1

def usage():
	print("python multiscanner.py -t <ipaaddress> -s <port> -e <port>")
	print("If no ip address is specified it will scan on 0.0.0.0")
	print("start port default <0>")
	print("Finish port default <65536>")
	print("Make sure you run the program as root")

def main():
	global target
	global start
	global end
	global fileName
	myqueue = queue.Queue()
	sthreads=[]
	try:
		opts, args = getopt.getopt(sys.argv[1:],"t:s:e:")
	except getopt.GetoptError as err:
		print(str(err))
		usage()
	print(opts)
	for o,a in opts:
		if o in("-t"):
			target=a
		elif o in("-s"):
			start=int(a)
		elif o in ("-e"):
			end=int(a)
		else:
			print("Unhandled argument passed....exiting")
			sys.exit(2)
		if(start>=end):
			print("Start port has to be less than end port")
			sys.exit(2)
		if(start<0 or end<0 or start > 65536 or end > 65536):
			print("Invalid start or end port")
			sys.exit(2)
	print("Beginning TCP scan on machine with IP ",target,"Ip port range ",start,"-",end)
	fileName=open("Host-ports-open.txt","w+")
	fileName.write("------------------------TCP PORTS------------------------\n")
	for i in range(start,end+1):
		myqueue.put(i)

	for i in range(1,10):
		t1 = ScannerThread(myqueue,i)
		t1.setDaemon(True)
		t1.start()
		sthreads.append(t1)

	myqueue.join()
	print("Finished TCP SYN Scanning")
	fileName.write("-------------------------\n\n")
	print("Initiating UDP Scaning")
	fileName.write("------------------------UDP PORTS------------------------\n")
	ports= range(start,end+1)
	UDPScan(ports)
	print("UDP port scanning finished")
	fileName.write("-------------------------\n\n")
	print("Initiating OS OSFingerPrinting")
	OSFingerPrinting()
	fileName.write("-------------------------\n\n")




if __name__ == '__main__':
	main()
