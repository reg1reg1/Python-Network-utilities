'''
Raw packet sniffing can be tough to do as it involves a lot of situation based bytes packing and unpacking 
(Using the struct C library)


Description: First Wifi Scapy script to print out first 10 received beacons' SSID's on a network (on a given channel), (may repeat)
Insight into how scapy works, uncomment the print lines to see how the value is being extracted.
IMP: It scans only for beacons on one channel.
Check the channel of your interface by iwconfig <iface-name> channel (1-11)
BEWARE there are certain regulations on what channel you are allowed to put your card on!!!
See the rules here: https://en.wikipedia.org/wiki/List_of_WLAN_channels under 2.4 GHz (802.11b/g/n/ax)
'''

from scapy.all import *
from pprint import pprint
from subprocess import Popen, PIPE, call

interface="wlan0mon"
channel =0
dev=set()
hiddendev=set()
count=0
#Note that card will only be able to sniff at one channel at a time
#Running this script and reading the output together will make a lot of things clearer about scapy object access

    
def handlePacket(pkt):
    #Checking if it is indeed a wireless packet
    global count
    global dev
    global hiddendev
    global channel
    
    radiotap=pkt.getlayer(0)
    field_names_list = [field.name for field in radiotap.fields_desc]
    fields = {field_name: getattr(radiotap,field_name) for field_name in field_names_list}
    
    channel = int(fields['Channel'])
    channelNo= int((channel-2412)/5)+1
    if pkt.haslayer(Dot11FCS):
        
        
        pktDot11FCS = pkt.getlayer(Dot11FCS)
        if pkt.type==0 and pkt.subtype==8:
            #print(pktDot11FCS.show()) 
            
            #Lists out the fields in a layer with index 2 
            #for a beacon frame that would be information element layer
            #first get field names, then use the names to access the values
            field_names_list = [field.name for field in pktDot11FCS.getlayer(2).fields_desc]
            #print(field_names_list)
            #create a dictionary object 
            
            
            fields = {field_name: getattr(pktDot11FCS.getlayer(2),field_name) for field_name in field_names_list}
            #print(fields)
            
            device=fields['info'].decode()
            #print("SSID:",fields['info'].decode())
            if pkt.info:
                dev.add((device,channelNo,pkt.addr3))
            else:
                hiddendev.add((device,channelNo,pkt.addr3))
            
            
            
            
            #print(pktDot11FCS.getlayer(2).getlayer(3))
            #print("##begin iteration")

#Scapy sniff is a blocking call hence it is recommmended to use thread for it
#Cannot thread  this as the card cannot be at 2 modes at a given time anyways
def sniffChannel(k):
    global interface
    global channel
    channel =k
    p = call(['iwconfig',interface,'channel',str(channel)], stdout=PIPE)
    
    #output = p.stdout.read()
    #print("Output:",output)
    packet=sniff(iface=interface,prn=handlePacket,filter="wlan type mgt subtype beacon",count=20,timeout=30)
    
def main():
    for i in range(1,12):
        sniffChannel(i)
    print("Visible Devices")
    for i in dev:
        print("::channel::",i[1],"::ssid::",i[0],"::bssid::",i[2])
    print("Devices with hidden SSID's")
    for i in hiddendev:
        print("Channel",i[1],"bssid::",i[2])
if __name__ == '__main__':
    main()

    
