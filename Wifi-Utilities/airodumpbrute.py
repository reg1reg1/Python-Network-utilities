'''
Decryption using airdecap-ng, written in python3

Can be done easily from the CLI and aircrack with the bruteforce option as well
'''

import sys, binascii, re
from subprocess import Popen, PIPE

f = open('rockyou.txt', 'r')
count =0
for line in f:

    wepKey = line.replace("\n","")
    if len(wepKey) not in [5,13,16,29,61], :
        continue
    
    hexKey = binascii.hexlify(wepKey.encode())
    print("Trying with WEP Key: " +wepKey+" Hex: ",hexKey)
    p = Popen(['airdecap-ng', '-w', hexKey.decode(), '<Insert PCAP file here>'], stdout=PIPE)
    #output = p.stdout.read()
    print(type(output))
    #output=output.decode()
    print(output)
    finalResult = output.split('\n')[5]
    if finalResult.find('1') != -1 :
        print("Key Match "  + wepKey)
        sys.exit(0)
    count+=1
print("No WEP key in file")
