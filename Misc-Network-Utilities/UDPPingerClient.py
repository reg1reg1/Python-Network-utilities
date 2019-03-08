import sys
import socket
import time
target_host="127.0.0.1"
target_port= 12000 #As mentioned in the server

client=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


client.settimeout(1)
sequence_number=1
minRTT=999
maxRTT=-1
count=0
sumRTT=0
print("---------------------BEGIN UDP PING------------------------------------")
while sequence_number<=10:
	
	currtime = time.clock() #For the increased precision time.clock() has been used
	msgtime = time.time()
	message= "Ping "+ str(sequence_number)+" "+str(msgtime)
	client.sendto(message.encode(),(target_host,target_port))
	
	try:
		data,addr = client.recvfrom(1024)
		
		data = data.decode()
		rettime= time.clock()
		
		RTTtime= rettime-currtime 
		maxRTT=max(maxRTT,RTTtime)
		minRTT= min(minRTT,RTTtime)
		sumRTT=sumRTT+RTTtime
		print("Message received: ", data," from ",addr)
		print("Round trip time: ",RTTtime,"seconds")
	
	except socket.timeout as e:
		print("Request timed out")
		count=count+1
	sequence_number = sequence_number+1

averageRTT = float(sumRTT/(10-count))
packetDrop =  (count/10)*100
print("------------------------UDP Exchange statistics-----------------------------")
print("The minRTT is ",minRTT)
print("The maxRTT is ",maxRTT)
print("The averageRTT is",averageRTT)
print("The packet drop rate is",packetDrop,"%")