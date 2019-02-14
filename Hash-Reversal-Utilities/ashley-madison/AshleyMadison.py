#!/usr/bin/python3
import hashlib
import time
print("Author: ys3334@nyu.edu")
print("Simulating an attack by reading from a wordList")
print("The file cracked.txt will contain all the cracked passwords")
#Load the Hashed Passwords into a Set

#Using time module to track program running time over password cracks
start = time.time()

passwordHashes = open('hash.dump', 'r',encoding='UTF8')
hashmd5Set = set()
dictionary = open('rockyou.txt','r',encoding='UTF8',errors="ignore")
crackedFile = open('crackedAshleyMadisonDictionary.txt', 'w+',encoding='UTF8')

testFile= open('hashdumpstore.txt','w+',encoding='UTF8')
testFile2= open('dict.txt','w+',encoding="UTF-8")

limit=1000 #limiting for cutting off execution
userList=[]
#Adding all the hashes recovered to a set to achieve fast lookup
for line in passwordHashes:
    x = line.replace("\n","").split(",")
    hashmd5Set.add(str(x[3][1:-1]))
    userList.append(x[1][1:-1])
    testFile.write(str(x[3][1:-1]))
    testFile2.write(str(x[3][1:-1]))
    #print(x[3][1:-1])
    #print(x[1][1:-1])

count=0
attempt=0
uscount=0
for users in userList:
    print("User check for$"+users+"$")
    uscount=uscount+1
    for items in dictionary:
        #print("entered")
        attempt=attempt+1
        plainConcat = str(users) + "::" + items.replace("\n","")
        md5verb = hashlib.md5(plainConcat.encode("utf-8"))
        testFile2.write(md5verb.hexdigest()+"\n")
        if md5verb.hexdigest() in hashmd5Set:
            str1= "User::"+users+ " ::Password: "+items+" \n"
            crackedFile.write(str1)
            count=count+1
            #print("Match Found ",match)
            break
    dictionary.seek(0,0)

print(attempt)
print(uscount)
print("Program terminated, cracked ",count," users")

