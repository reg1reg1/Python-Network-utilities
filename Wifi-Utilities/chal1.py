import os
import codecs
#Insert rc4 implementation here
'''
Plaintext given: 
Going from AP to station: Challenge text (packet 1)

Challenge text: 128 bytes: 8b12e819a3cd911776edf7c3cd5c5e0f1cc10742f2dc998a3538e5a3b0b6af3c8412c3b2a8cdf789fae2e4f244504011fdc467028aee51632cd0476827a7bb8bcc2d0c41b62b12135f3cc26306216d1184ba1c97553f7924dd153ada3bc3c69ba8a21c77931fe9677dbcb916625d58b5ee9ae9615b01f73811178bfd8ab5b69a

Encryption text: 136 bytes: 70caef5c0b096c6d2e0bbed6b1c510fd2536bd6dbb765d277e471e9b0e892988038bf62b266f3fbb0935f050c7aec046cedccea852073bca42b3b971ca6898c8ec845d24b09b712b2b4f091abb43bca4562815d685e4c600707f13b8f2caa2c33ef07f785ee12ac4a06cd88dc0d1c8bf15a75518c3db593d2b2869ab6c86a5e8964d6d1b1f67e41c"


ICV Value:(for the challenge text) 4bytes
ca8aa281

IV value: (For the challenge text)
3a6f63


IV for the Data: (Not same and hence we don't have a valid keystream corresponding to this IV, the only option that remains now is to
bruteforce a common list of WEP passkeys)
c9b15f
ICV for the Data:
50780e71

Data (Encrypted):




Size in bytes of the challenge text: (This is plaintext), the client has to encrypt it and and send it back to the AP. The AP then verifies whether that packet has been encrypted correctly and allows the client to authenticate



'''



import sys
import binascii
from rc4 import decrypt, encrypt
from arc4 import ARC4

MOD = 256

challengeText="8b12e819a3cd911776edf7c3cd5c5e0f1cc10742f2dc998a3538e5a3b0b6af3c8412c3b2a8cdf789fae2e4f244504011fdc467028aee51632cd0476827a7bb8bcc2d0c41b62b12135f3cc26306216d1184ba1c97553f7924dd153ada3bc3c69ba8a21c77931fe9677dbcb916625d58b5ee9ae9615b01f73811178bfd8ab5b69a"

encryptedText="70caef5c0b096c6d2e0bbed6b1c510fd2536bd6dbb765d277e471e9b0e892988038bf62b266f3fbb0935f050c7aec046cedccea852073bca42b3b971ca6898c8ec845d24b09b712b2b4f091abb43bca4562815d685e4c600707f13b8f2caa2c33ef07f785ee12ac4a06cd88dc0d1c8bf15a75518c3db593d2b2869ab6c86a5e8964d6d1b1f67e41c"

chalICV="ca8aa281"

chalIV="3a6f63"

guessKey="tudes"


#Insert rc4 implementation here




    

def testKey(key,cText,encText):
    global chalIV
    #rc4Input is a String type representing hexadecimal characters
    rc4Input = binascii.hexlify(key.encode()).decode()+chalIV
    #Not sure about direction of concatenation
    rc4str= ":octudes"
    rc4str2="tudes:oc" 
    


testKey(guessKey,challengeText,encryptedText)

    

