'''
Resolving hidden ssid's by probing requests when a client connects with it.
There is an additional way of dictionary attack to reveal the essid as well.
'''
import sys
import os
from scapy.all import *
from pprint import pprint
from subprocess import Popen, PIPE, call

interface = "wlan0mon"
dev = set()

def handlePacket(pkt):
    if pkt.haslayer(Dot11Beacon):
        if not pkt.info:
            if pkt.addr3 not in dev:
                dev.add(pkt.addr3)
                print("Hidden Network found with bssid",pkt.addr3)
                
    elif pkt.haslayer(Dot11ProbeResp) and (pkt.addr3 in dev):
        print("Hidden SSid uncovered",pkt.info.decode(),"which had bssid",pkt.addr3.decode())
        

def sniffHiddenSsid(k):
    global interface
    channel = k
    p = call(['iwconfig',interface,'channel',str(channel)], stdout=PIPE)
    packet=sniff(iface=interface,prn=handlePacket,count=20,timeout=30)

def main():
    #sniff for beacons on every channel
    for i in range(1,12):
        sniffHiddenSsid(i)
if __name__ == '__main__':
    main()
