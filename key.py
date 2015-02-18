#Michael Quinn Parkinson- Creates a "Key"
# the key will be used to generate a random permutation of a string
#This file will be used to encrypt a string later on.
# The additional file is the crypt.py
import random
import string
##Write File
# A lot of Possible options
Alpha_Lower = list(string.ascii_lowercase)
Alpha_Lower.extend([" " , "," , "." , ";" , "'" , "!" , "@" , "#" , "$" , "%" , "^" , "&" , "*" , "(" , ")" , ":" , ">" , "<" , "?" , "|" ,"~","`","+","=","_","-","1","2","3","4","5","6","7","8","9","0"])
# The code can be anything length strength.
# the longer the string the harder it will be to guess what the key is.
Code = raw_input("\nEnter The Key Code...\n \n")
Code = ''.join(['%08d'%int(bin(ord(i))[2:]) for i in str(Code)])
#
#The seed for the RNG is the code
def CreateCrypt(Alpha_Lower,Code):
    random.seed(int(Code))
    Store = []
    for i in range(len(Alpha_Lower)):
        x = random.random()
        if x in Store:
            continue
        else:
            Store.extend([x])
    return Store

Store = CreateCrypt(Alpha_Lower,Code)
# Saves the key to the folder this file is in.   
with open("key","w+") as file:
    for i in range(len(Store)):
        file.write(str(Store[i])+"\n")
    file.close()
