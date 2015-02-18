# Michael Quinn Parkinson - Cracks encrypted data.
# This is the code that will reverse the encryption process
#defined in the crypt.py file. This script will use both
#keys to "unlock" the encryption and display the result.
import string
import sys
import os
Alpha_Lower = list(string.ascii_lowercase)
Alpha_Lower.extend([" " , "," , "." , ";" , "'" , "!" , "@" , "#" , "$" , "%" , "^" , "&" , "*" , "(" , ")" , ":" , ">" , "<" , "?" , "|" ,"~","`","+","=","_","-","1","2","3","4","5","6","7","8","9","0"])
Alpha_Upper =  list(string.ascii_uppercase)

# Opens the generation key.
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

#opens the encrypted data.    
try:
    with open("crypt","r") as file:
        Cryptic = []
        data = file.readlines()
        for i in range(len(data)):
            tmp = data[i]
            Cryptic.extend([tmp[:-1]])
except IOError:
    "\nNo File\n"
    sys.exit()

# Stores the encrypted data
def Crack(Cryptic,Store,Alpha_Lower,Alpha_Upper):
    String = []
    try:
        for i in range(len(Cryptic)):
            if Cryptic[i] in Store:
                ind = Store.index(Cryptic[i])
                String.extend([Alpha_Lower[ind]])
    except TypeError:
        pass
    return String
# Puts the data into the correct order
def UnShuffle(Cryptic):
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
#Cryptic = UnShuffle(Cryptic)
String = Crack(Cryptic,Store,Alpha_Lower,Alpha_Upper)

if len(String) != 0:
    with open("crack","w+") as file:
        file.write(''.join(String))
        file.close()
    os.remove(os.path.abspath("key"))
    os.remove(os.path.abspath("crypt"))
else:
    os.remove(os.path.abspath("key"))
        
