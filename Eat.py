# Michael Quinn Parkinson - Non-Interactive RNG Fighter
# This is a fun program that randomly generates fights between the player and a monster. The program is ran and you get to see how far you can get.
# The program starts off with a low monster health and damage but quickly picks up the pace.
# There is no real point to this program other than just creating it for fun and experience.
# The Player starts off a little bit stronger than the monsters.

import random
import time

life = 100.0    #Initial Life
MLife = life    # Monster Life
PLife = life-25    # Player Life

PStr = 5    #Initial Player Strength Modifier. This determines the amount of damage the player can do.
MStr = 4    #Initial Monster strength Modifier. This determines the amount of damage the monster can do.

xp = 0  #Inital player experience. To level up a character you need 1.5 Times the current player to advance.
level = 1   #The Player starts at level 1.

# Loop the game until the players health drops below zero

print "\nWELCOME!\n"
while PLife > 0:
    att = random.random()   # random attack speed between 0 and 1
    hitP = random.random()  #random Player hit chance between 0 and 1
    hitM = random.random()  #random Monsters hit chance between 0 and 1
    if hitP > 1 - hitM: # When this is satified the player will succesfully attack.
        crit = random.random()  #critical hit modifier
        if crit >= 0.95:    #All crit rolls can stack to create criticals of critical hits
            print "\nCRITICAL HIT!\n"   
            dam = random.uniform(1,PStr)*random.uniform(1,PStr)
            print "\nThe Player Attacks For" ,dam , '\n'
            crit = random.random()
            MLife -= dam    # Decrease the monster life with the player damage.
            print "\n The Monster Has ", MLife, "Left \n"
            if crit > 0.975:
                print "\nDOUBLE CRITICAL HIT!\n"
                dam += random.uniform(1,PStr)*random.uniform(1,PStr)
                print "\nThe Player Attacks For" ,dam , '\n'
                crit = random.random()
                MLife -= dam
                print "\n The Monster Has ", MLife, "Left \n"
                if crit > 0.9875:
                    print "\nTRIPLE CRITICAL HIT!\n"
                    dam += random.uniform(1,PStr)*random.uniform(1,PStr)
                    print "\nThe Player Attacks For" ,dam , '\n'
                    crit = random.random()
                    MLife -= dam
                    print "\n The Monster Has ", MLife, "Left \n"
                    if crit > 0.99375:
                        print "\nQUATRA CRITICAL HIT!\n"
                        dam += random.uniform(1,PStr)*random.uniform(1,PStr)
                        print "\nThe Player Attacks For" ,dam , '\n'
                        crit = random.random()
                        MLife -= dam
                        print "\n The Monster Has ", MLife, "Left \n"
                        if crit > 0.996875:
                            time.sleep(5)
                            print "\nP-P-P-P-PENTA CRITICAL HIT!\n"
                            dam += random.uniform(1,PStr)*random.uniform(1,PStr)
                            print "\nThe Player Attacks For" ,dam , '\n'
                            MLife -= dam
                            print "\n The Monster Has ", MLife, "Left \n"
        else:   #if the player does not ciritically hit then the player does the normal amount of damage determined by the strength.
            dam = random.uniform(1,PStr)
            print "\nThe Player Attacks For" ,dam , '\n'
            time.sleep(att) #The amount of time for each attack is the attack speed
            MLife -= dam    # Decrease the monster life with the player damage.
            print "\n The Monster Has ", MLife, "Left \n"
    if MLife > 0:   # The monster roll is the same as the player roll
        if hitM > 1-hitP:   # The monster attacks succesfully when the attack roll is satisfied 
            crit = random.random()
            if crit >= 0.95:
                print "\nCRITICAL HIT!\n"
                dam = random.uniform(1,MStr)*random.uniform(1,MStr)
                print "\nThe Monster Attacks For ", dam, "\n"
                crit = random.random()
                PLife -= dam
                print "The Player Has ", PLife, "Left\n"
                if crit > 0.975:
                    print "\nDOUBLE CRITICAL HIT!\n"
                    dam += random.uniform(1,MStr)*random.uniform(1,MStr)
                    print "\nThe Monster Attacks For ", dam, "\n"
                    crit = random.random()
                    PLife -= dam
                    print "The Player Has ", PLife, "Left\n"
                    if crit > 0.9875:
                        print "\nTRIPLE CRITICAL HIT!\n"
                        dam += random.uniform(1,MStr)*random.uniform(1,MStr)
                        print "\nThe Monster Attacks For ", dam, "\n"
                        crit = random.random()
                        PLife -= dam
                        print "The Player Has ", PLife, "Left\n"
                        if crit > 0.99375:
                            print "\nQUATRA CRITICAL HIT!\n"
                            dam += random.uniform(1,MStr)*random.uniform(1,MStr)
                            print "\nThe Monster Attacks For ", dam, "\n"
                            crit = random.random()
                            PLife -= dam
                            print "The Player Has ", PLife, "Left\n"
                            if crit > 0.996875:
                                time.sleep(5)
                                print "\nP-P-P-P-PENTA CRITICAL HIT!\n"
                                dam += random.uniform(1,MStr)*random.uniform(1,MStr)
                                crit = random.random()	
                                PLife -= dam
                                print "The Player Has ", PLife, "Left\n"		
            else:
                dam = random.uniform(1,MStr)
                print "\nThe Monster Attacks For ", dam, "\n"
                time.sleep(att)
                PLife -= dam
                print "The Player Has ", PLife, "Left\n"
    if MLife <= 0:  # This is satisfied when the monster's hit points are less than or equal to zero
        print "The Monster Has Died.\n"
        xp += random.random()# When the monster dies experience is rewarded to the player
        PLife = life #The player heals
        MLife = life/(random.uniform(1,5))  #creates a new monster to fight
    if PLife <= 0:  # When the player dies the game is done
        break   #breaks from the loop to give the death message
    if xp > level**(1.5):   #when the amount of experience exceeds 1.5*level the player increases its level.
        print "\n"
        print "\nLEVEL UP\n"
        time.sleep(0.25)
        level += 1
        print "Current Level: ", level
        life += 25.0	#Each level the player's health increases.
        PLife = life
        PStr +=  1 + random.random()   #each level the player's strength increases.
        MLife = life    #Increase the monster's health on player level up.
        MStr += 1+ random.random()  # Increases the monster damage when the player levels up.
print "\nPlayer Has Died\n"
print "Player Level ", level, "with ", xp, "experience\n"
