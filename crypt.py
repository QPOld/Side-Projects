#Michael Quinn Parkinson - Encrypts a string with the key.
# This program will use the key to generate a set of random 
#numbers to be the encryption.
# Another key will be made that will permuated the encryption.
# Thus an encrypted word is doubly protected with
# the generation key and the permutation key.
# To crack the encryption you need both keys.

import string
import random
import sys
import os
# An Array of possible symbols to be used.
Alpha_Lower = list(string.ascii_lowercase)
Alpha_Lower.extend([" " , "," , "." , ";" , "'" , "!" , "@" , "#" , "$" , "%" , "^" , "&" , "*" , "(" , ")" , ":" , ">" , "<" , "?" , "|" ,"~","`","+","=","_","-","1","2","3","4","5","6","7","8","9","0"])
Alpha_Upper =  list(string.ascii_uppercase)

#Reads in the key to be used.
try:
    with open("key","r") as file:
        Store = []
        data = file.readlines()
        for i in range(len(data)):
            tmp = data[i]
            Store.extend([tmp[:-1]])
except IOError:
    print "\nNo File\n"
    sys.exit()

# The word can also be a string.
# It creates a file with random data as well as the 
# encrypted word to increases the number of possible 
# permutations of the entire data set. This way to brute
# force the encryption will take significantly longer.
def Cryptic(Store,Alpha_Lower,Alpha_Upper):
    String = raw_input("\nWhat Word?\n \n")
    Str_Array = list(String)
    Cryptic = []
    for j in range(len(Str_Array)+random.randint(20,50)):
        Cryptic.extend([random.random()])
        try:
            Cryptic.extend([random.random()])
            if Str_Array[j] in Alpha_Lower:
                Cryptic.extend([random.random()])
                ind = Alpha_Lower.index(Str_Array[j])
                Cryptic.extend([random.random()])
                Cryptic.extend([Store[ind]])
                Cryptic.extend([random.random()])
            if Str_Array[j] in Alpha_Upper:
                Cryptic.extend([random.random()])
                ind = Alpha_Upper.index(Str_Array[j])
                Cryptic.extend([random.random()])
                Cryptic.extend([Store[ind]])
                Cryptic.extend([random.random()])
            else:
                Cryptic.extend([random.random()])
        except IndexError:
            Cryptic.extend([random.random()])
    return Cryptic
# It uses the key to shuffle the encrypted data.
# This protects the instance when the original key 
# is found. This way the word/string have two keys 
# for protection.
def Shuffle(Cryptic):
    Code = raw_input("\nEnter The Key Code...\n \n")
    Code = ''.join(['%08d'%int(bin(ord(i))[2:]) for i in str(Code)])
    random.seed(Code)
    shuffle = []
    Crypt = []
    for i in range(len(Cryptic)):
        shuf = random.randint(0,len(Cryptic))
        if shuf not in shuffle:
            shuffle[i] = shuf
    for j in range(len(Cryptic)):
        Crypt[i] = Cryptic[shuffle[i]]
    return Crypt
Cryptic = Cryptic(Store,Alpha_Lower,Alpha_Upper)
Crypt = Shuffle(Cryptic)
# Creates a regular file with the data.
# No point to hide data that can not be cracked 
#with out the generation key and permutation key.
with open("crypt","w+") as file:
    for i in range(len(Crypt)):
        file.write(str(Crypt[i])+"\n")
    file.close()
os.remove(os.path.abspath("key"))
