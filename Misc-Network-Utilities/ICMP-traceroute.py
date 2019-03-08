'''
---------------------------------------------------------------------------------
* Author: ys3334@nyu.edu                                                          *
* Title: ICMP pinger using raw Sockets                                            *
* Description:                                                                    *
* > Programmed to be run on 2.7.x as the sockets handle strings not bytes         *
* > Non-threaded                                                                  *
* > Trace routes servers from 4 continents with 4 packets each                    *
* > Trace route Ping timeout has a value of 4 seconds                             *
* > Usage: py ./ICMPPingerClient.py (Windows)                                     *
* > Written and tested on Windows(10) and Linux(Debian Distros)                   *
---------------------------------------------------------------------------------
'''
from __future__ import print_function
import os
from socket import * 
import sys
import struct
import time
import select
import binascii
ICMP_ECHO_REQUEST = 8
MAX_HOPS = 30
TIMEOUT =2.0
TRIES = 5
# The packet that we shall send to each router along the path is the ICMP echo
# request packet, which is exactly what we had used in the ICMP ping exercise.
# We shall use the same packet that we built in the Ping exercise
def checksum(string):
	csum = 0
	countTo = (len(string) // 2) * 2
	count = 0
	while count < countTo:
		thisVal = ord(string[count+1]) * 256 + ord(string[count])
		csum = csum + thisVal
		csum = csum & 0xffffffffL
		count = count + 2
	if countTo < len(string):
		csum = csum + ord(string[len(string) - 1])
		csum = csum & 0xffffffffL
	csum = (csum >> 16) + (csum & 0xffff)
	csum = csum + (csum >> 16)
	answer = ~csum
	answer = answer & 0xffff 
	answer = answer >> 8 | (answer << 8 & 0xff00)
	return answer
def build_packet():
	ID = os.getpid() & 0xFFFF
	myChecksum=0
	data = struct.pack("d", time.time())
	header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
	# Calculate the checksum on the data and the dummy header.
	myChecksum = checksum(str(header + data))
	# Get the right checksum, and put in the header
	
	if sys.platform == 'darwin':
	# Convert 16-bit integers from host to network byte order
		myChecksum = htons(myChecksum) & 0xffff
	else:
		myChecksum = htons(myChecksum)
	header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
	packet = header + data
 	return packet
def getDomainName(hostip):
	try:
		host = gethostbyaddr(hostip)
		hostName = nameorip = '{0} ({1})'.format(hostip , host[0]) 
	except Exception:
		hostName = '{0} (host name could not be determined)'.format(hostip) 
	return hostName
def get_route(hostname):
	timeLeft = TIMEOUT
	for ttl in range(1,MAX_HOPS):
		for tries in range(TRIES):
			icmp = getprotobyname("icmp")
			destAddr = gethostbyname(hostname)
			mySocket = socket(AF_INET, SOCK_RAW, icmp)
			mySocket.setsockopt(IPPROTO_IP, IP_TTL, struct.pack('I', ttl))
			mySocket.settimeout(TIMEOUT)
			try:
				d = build_packet()
				mySocket.sendto(d, (hostname, 0))
				t= time.time()
				startedSelect = time.time()
				whatReady = select.select([mySocket], [], [], timeLeft)
				howLongInSelect = (time.time() - startedSelect)
				if whatReady[0] == []: # Timeout
					print(" * * * Request timed out.")
				recvPacket, addr = mySocket.recvfrom(1024)
				timeReceived = time.time()
				timeLeft = timeLeft - howLongInSelect
				if timeLeft <= 0:
					print(" * * * Request timed out.")
			except timeout:
				continue
			else:
				ipheader= struct.unpack("BBHHHBBH4s4s",recvPacket[:20])
				
				srcIp= inet_ntoa(ipheader[8])
				destIp= inet_ntoa(ipheader[9])
				types,code,checksum,packID,sequence = struct.unpack("bbHHh",recvPacket[20:20+struct.calcsize("bbHHh")])
				#print("Reply from ",srcIp,", ttl= ",ipheader[5] , ", sequencenumber= ",sequence,", checksum= ",checksum,",time=",end=" ")
				hostName = getDomainName(addr[0])
				if types == 11:
					bytes = struct.calcsize("d")
					timeSent = struct.unpack("d", recvPacket[28:28 +bytes])[0]
					print(" %d rtt=%.0f ms %s" %(ttl,(timeReceived -t)*1000, hostName))
				elif types == 3:
					bytes = struct.calcsize("d")
					timeSent = struct.unpack("d", recvPacket[28:28 +bytes])[0]
					print(" %d rtt=%.0f ms %s" %(ttl,(timeReceived-t)*1000, hostName))
				elif types == 0:
					bytes = struct.calcsize("d")
					timeSent = struct.unpack("d", recvPacket[28:28 +bytes])[0]
					print(" %d rtt=%.0f ms %s" %(ttl,(timeReceived - timeSent)*1000, hostName))
					return
				else:
					print("error")
				break
			finally:
				mySocket.close()
def main():
	print("Tracerouting servers")
	#Google server United States
	print("**************google.com*******************") 
	get_route("google.com")

	print("******speedtest.mel01.softlayer.com********")
	get_route("speedtest.mel01.softlayer.com")

	print("**************Proxy Netherlands************")
	get_route("146.185.157.238")

	print("**************Proxy South Africa************")
	get_route("154.73.159.10")

if __name__ == '__main__':
	main()