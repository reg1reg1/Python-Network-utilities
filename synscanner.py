import sys
import getopt
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
import queue
import threading
import time

'''
Multithreaded tcp SYN scanner
It scans for port scans 
A port which is open might not necessarily send "SYN-ACK"
A firewall may cause a silent drop
Hence such an assumption cannot be made.
'''
target="0.0.0.0"
start=0
end=65536


class ScannerThread(threading.Thread):
	def __init__(self,queue,tid):
		threading.Thread.__init__(self)
		self.tid=tid
		self.queue=queue
		
	def run(self):
		global target
		total_ports=0
		ipaddress=sys.argv[1]
		while True:
			try:
				#print(self.queue.qsize())
				port = self.queue.get(timeout=1)
			except queue.Empty:
				print("Queue is empty, thread-",self.tid," exiting......")
				return
			response=sr1(IP(dst=target)/TCP(sport=8080,dport=port,flags="S"),verbose=False,timeout=5)
			if response:
				if response[TCP].flags==18:
					print("Thread-",self.tid," found port ",port," to be open")
				else:
					print("Thread-",self.tid," found port ",port,"to be closed")
			self.queue.task_done()
			total_ports+=1

def usage():
	print("py synscanner.py -t <ipaaddress> -s <port> -e <port>")
	print("If no ip address is specified it will scan on 0.0.0.0")
	print("start port default <0>")
	print("Finish port default <65536>")

def main():
	global target
	global start
	global end

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
			print("entered")
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
	for i in range(start,end+1):
		myqueue.put(i)

	for i in range(1,10):
		t1 = ScannerThread(myqueue,i)
		t1.setDaemon(True)
		t1.start()
		sthreads.append(t1)

	myqueue.join()

	for items in sthreads:
		item.join()

	print("Finished Scanning")

if __name__ == '__main__':
	main()