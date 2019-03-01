import sys
import threading
import socket
import datetime


def server_loop(hostloc,portloc,remotehost,remoteport,isReceive):
	#creating a socket of type TCP
	server =socket.socket(socket.AF_INET,socket.SOCK_STREAM)

	#local client must connect tothis tcp proxy server
	try:
		server.bind((hostloc,portloc))
		print "Tcp proxy Server listening on ",hostloc," ",portloc
	except Exception as e:
		print "<line17>Server failed to listen on the  specified port/host pair, exiting....",e
		sys.exit(0)


	#Listening to atmost 3 concurrent connections. 
	server.listen(3)

	while True:
		print "Proxy Server listening for connections from clients...." 
		#blocking code till server.accept() returns
		client_sock,addr = server.accept()
		#client_sock now has the details of the client socket that connected to server
		print "Client connection initiated with client at",addr[0]," at port ",addr[1]
		tcpthread = threading.Thread(target=proxyhandler,args=(client_sock,remotehost,remoteport,isReceive))
		tcpthread.start()




def proxyhandler(clientSock,host,port,isReceive):

	#connect to remote host
	remoteDev = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	remoteDev.connect((host,port))
	print "Connected to remote server at ",host," ",port
	clientSock.send("Was successfully able to connect to remote server.....")
	#receive data from the remote end if necessary
	#recv_from vs recv (See python documentation)
	if isReceive:
		#receiving response from remote
		response_remote = receive_from_socket(remoteDev,0)
		print "Receiving data from remote server as ", response_remote
		dumphexVal(response_remote)
		
		#handling the response from remote and handling it, sending it to client
		#If you want to tamper/modify  with the response sent from remote, do it here
		response_remote =  response_handler(response_remote)
		#if we have something to send to our local client
		if(len(response_remote)):
			print "Sending data from remote server to local client....." 
			clientSock.send(response_remote)

		#lather,rinse,repeat
		'''
		1)Receive data from client
		2)Send to remote
		3)Receive response from remote
		4)Send to client
		'''
	while True:
		#1)read from local client
		local_data = receive_from_socket(clientSock,1)
		print "Data received from local ",local_data
		isSomeResponseFlag=False
		if(len(local_data)):
				
			isSomeResponseFlag=True
			#2)Send request received from client to remote
			print "Sending %s of len %d bytes to remote server",local_data,len(local_data)
				
			dumphexVal(local_data)

			#Modify the request if any for remote host

			local_data = request_handler(local_data)
			remoteDev.send(local_data)

			print "Data [: %s] sent to remote" %(local_data)
			#3)Receive response from remote
			response_remote = receive_from_socket(remoteDev,0)

		if(len(response_remote)):
			isSomeResponseFlag=True
			print "Sending %s of length %d bytes to client" %(response_remote,len(response_remote))
			dumphexVal(response_remote)

			#Modify the request if any to remote host

			response_remote = response_handler(response_remote)

			clientSock.send(response_remote)

			print "Data [: %s] sent to client" %(response_remote)

		if(isSomeResponseFlag is False):
			print "No more data to send or receive closing the connections...." 
			remoteDev.close()
			clientSock.close()
			print "connections closed" 
			break

#Plain oldschool tcp receive from socket
def receive_from_socket(socketObject,x):
# python .\tcPProxyservice.py 127.0.0.1 9000 192.168.1.8 8000 True
	if x==0 :
		print "Receiving from remote server" 
	else:
		print "Receiving from client"
	#Setting a timeout of 3s
	#socketObject.settimeout(3);
	resp=""
	resplen=1
	try:
		while True:
			print "Inside proxy recv_from socket function" 
			respbuffer = socketObject.recv(4096)
			resplen= len(respbuffer)
			resp+=respbuffer
			if resplen < 4096:
				break
			print "Inside proxy recv_from socket function response receive length %d" %(resplen)
	except Exception as e:
		print "Exception detected as<line 123>",e
		pass
	return resp

def dumphexVal(src):
	pass
def request_handler(req):
	#tamper/modify
	return req

def response_handler(resp):
	#tamper
	return resp
#--help on wrong usage
def Usage():
	print "TCPproxy v1.0" 
	print "eg: ./tcPProxyservice.py <localIp> <port> <remoteIp> <remoteport> True/False" 
	print "The fifth parameter true needs to be set when interacting with remote hosts," 
	print "that send data before connecting(some FTP services)" 
	sys.exit(0)


#the main function
def main():
	print "entered  main" 
	if (len(sys.argv[1:])!=5):
		print "Invalid Argument length, exiting....." 
		Usage()
		sys.exit(0)

		#Simple command line parsing
	localhost = sys.argv[1]
	localport = int(sys.argv[2])
	remotehost = sys.argv[3]
	remoteport = int(sys.argv[4])

	isReceiveTrue = bool(sys.argv[5])
	#Call the server loop to start listening
	server_loop(localhost,localport,remotehost,remoteport,isReceiveTrue)
	print "Main exiting...." 

main()
		














