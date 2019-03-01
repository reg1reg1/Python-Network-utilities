#!/usr/bin/python3
import hashlib
import time
print("Author: ys3334@nyu.edu")
print("Simulating a dictionary attack by reading from a wordList")
print("The file cracked.txt will contain all the cracked passwords")
#Load the Hashed Passwords into a Set

#Using time module to track program running time over password cracks
start = time.time()

passwordHashes = open('formspring.txt', 'r',encoding='UTF8')
hash256Set = set()
dictionary = open('rockyou.txt', 'r',encoding='UTF8')
crackedFile = open('cracked.txt', 'w+',encoding='UTF8')



limit=1000 #limiting for cutting off execution

#Adding all the hashes recovered to a set to achieve fast lookup
for line in passwordHashes:
	hash256Set.add(line.replace("\n","")) 
y = [chr(x+48) for x in range(10)]
x=0
crackedFile.write("Cracked "+str(limit)+"passwords\n")
for line in dictionary:
    for i in y:
        for j in y:
            #Adding salt in tens and units places in the dictionary
            saltedPlaintext = j + i + line.replace("\n","")
            #print(saltedPlaintext)
            #hashed using SHA-256(Information on the hashing mechanism was fetched online)
            sha256Text = hashlib.sha256(saltedPlaintext.encode("utf-8"))
	    #searching for a hashMap using a Set datastructure	
            if sha256Text.hexdigest() in hash256Set:
                crackedFile.write("hash::"+sha256Text.hexdigest()+ "::pass::" +line.replace("\n","")+"::salt::"+str(i+j)+"\n")
                limit=limit-1
                print(limit)
                #print("Debug: Match Found!!!!!")
    if limit<=0:
        break
	
endTime=time.time()

print("Took "+" "+endTime-startTime+" seconds")
crackedFile.write("Finished execution in "+str(endTime-startTime)+" seconds")
